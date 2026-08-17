"""Fail-closed reader for persistent authority and ephemeral runtime leases.

Only the JSON enclosed by the exact markers in PROJECT_STATUS.md grants
persistent operational state. Execution additionally requires a fresh runtime
lease outside Git, bound to the already-published repository HEADs.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping


AUTHORITY_BEGIN = "<!-- AI_DEV_OS_OPERATIONAL_AUTHORITY_BEGIN -->"
AUTHORITY_END = "<!-- AI_DEV_OS_OPERATIONAL_AUTHORITY_END -->"
DEFAULT_STATUS_FILE = Path(__file__).with_name("PROJECT_STATUS.md")
DEFAULT_AUTHORITY_LEASE_FILE = Path(
    r"C:\developments\archive\ai-dev-os-runtime\projects\melomanos\authority\active-authority-lease.json"
)
UTC = timezone.utc
MAX_AUTHORITY_LIFETIME = timedelta(hours=72)
MAX_ISSUED_FUTURE_SKEW = timedelta(minutes=5)
HEAD_NAMES = ("workspace", "backend", "frontend", "ai_dev_os")
HEAD_PATTERN = re.compile(r"^[0-9a-f]{40}$")

# Fixed vocabularies prevent subordinate documents from minting authority.
KNOWN_MODES = frozenset(
    {"read_only_audit", "governance_only", "product_implementation", "release"}
)
KNOWN_ACTIONS = frozenset(
    {
        "governance_docs",
        "governance_scripts",
        "governance_tests",
        "read_only_inspection",
        "product_code",
        "product_tests",
        "product_build",
        "server",
        "network",
        "cloud",
        "secrets",
        "database",
        "deployment",
        "stage",
        "commit",
        "push",
        "merge",
        "pull_request",
        "publication",
        "roadmap_promotion",
        "status_write",
        "build",
        "test",
    }
)
PERSISTENT_AUTHORITY_FIELDS = frozenset(
    {
        "schema_version",
        "authority_file",
        "authority_revision",
        "authorized_mission",
        "held_missions",
        "completed_missions",
        "m021",
        "bounties",
        "production_deployment",
        "allowed_actions",
        "forbidden_actions",
    }
)
LEASE_FIELDS = frozenset(
    {
        "lease_schema_version",
        "lease_id",
        "authority_revision",
        "mission_id",
        "mode",
        "allowed_actions",
        "issued_at_utc",
        "expires_at_utc",
        "expected_heads",
    }
)


class AuthorityError(ValueError):
    """Raised when authority or a required lease is invalid or insufficient."""


@dataclass(frozen=True)
class AuthorizedMission:
    """The single mission that the persistent authority permits."""

    mission_id: str
    status: str
    mode: str
    allowed_actions: tuple[str, ...]
    forbidden_actions: tuple[str, ...]


@dataclass(frozen=True)
class OperationalAuthority:
    """Validated persistent canonical operational state, with no lease data."""

    authority_file: str
    authority_revision: int
    mission: AuthorizedMission
    raw: dict[str, Any]


@dataclass(frozen=True)
class RuntimeLease:
    """Validated ephemeral execution lease, stored outside all repositories."""

    lease_id: str
    authority_revision: int
    mission_id: str
    mode: str
    allowed_actions: tuple[str, ...]
    issued_at_utc: datetime
    expires_at_utc: datetime
    expected_heads: dict[str, str]


def _one_marker(text: str, marker: str) -> int:
    count = text.count(marker)
    if count != 1:
        raise AuthorityError(f"Expected exactly one {marker!r} marker; found {count}.")
    return text.index(marker)


def extract_authority_json(text: str) -> str:
    """Return the one JSON payload enclosed by the canonical exact markers."""

    begin = _one_marker(text, AUTHORITY_BEGIN)
    end = _one_marker(text, AUTHORITY_END)
    if end <= begin:
        raise AuthorityError("Operational authority markers are out of order.")
    payload = text[begin + len(AUTHORITY_BEGIN) : end].strip()
    if not payload:
        raise AuthorityError("Operational authority block is empty.")
    return payload


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AuthorityError(f"Duplicate JSON key: {key!r}.")
        result[key] = value
    return result


def _json_object(text: str, description: str) -> dict[str, Any]:
    try:
        raw = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except json.JSONDecodeError as error:
        raise AuthorityError(f"Malformed {description} JSON: {error.msg}.") from error
    if not isinstance(raw, dict):
        raise AuthorityError(f"{description.capitalize()} JSON must be an object.")
    return raw


def _exact_fields(raw: Mapping[str, Any], expected: frozenset[str], description: str) -> None:
    if set(raw) != expected:
        missing = sorted(expected - set(raw))
        unexpected = sorted(set(raw) - expected)
        raise AuthorityError(
            f"{description} fields are invalid; missing={missing!r}, unexpected={unexpected!r}."
        )


def _string_list(value: Any, name: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise AuthorityError(f"{name} must be a non-empty list of action strings.")
    normalized = tuple(value)
    if len(set(normalized)) != len(normalized):
        raise AuthorityError(f"{name} contains duplicate actions.")
    unknown = set(normalized) - KNOWN_ACTIONS
    if unknown:
        raise AuthorityError(f"{name} contains unknown action classes: {sorted(unknown)!r}.")
    return normalized


def _timestamp(value: Any, name: str) -> datetime:
    if not isinstance(value, str):
        raise AuthorityError(f"{name} must be a UTC timestamp ending in Z.")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except ValueError as error:
        raise AuthorityError(f"{name} is malformed.") from error
    if parsed.strftime("%Y-%m-%dT%H:%M:%SZ") != value:
        raise AuthorityError(f"{name} is malformed.")
    return parsed


def _expected_heads(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        raise AuthorityError("expected_heads must be an object.")
    if set(value) != set(HEAD_NAMES):
        raise AuthorityError(
            "expected_heads must contain exactly workspace, backend, frontend, and ai_dev_os."
        )
    result: dict[str, str] = {}
    for name in HEAD_NAMES:
        head = value[name]
        if not isinstance(head, str) or not HEAD_PATTERN.fullmatch(head):
            raise AuthorityError(
                f"expected_heads.{name} must be a lowercase 40-character Git HEAD."
            )
        result[name] = head
    return result


def _mission_history(value: Any, name: str) -> None:
    if not isinstance(value, list):
        raise AuthorityError(f"{name} must be a list.")
    for item in value:
        if not isinstance(item, dict):
            raise AuthorityError(f"{name} entries must be objects.")
        mission_id = item.get("id")
        status = item.get("status")
        if not isinstance(mission_id, str) or not mission_id.strip() or not isinstance(status, str) or not status.strip():
            raise AuthorityError(f"{name} entries require non-empty id and status.")


def parse_authority_text(text: str) -> OperationalAuthority:
    """Parse and structurally validate schema-v2 persistent authority text."""

    raw = _json_object(extract_authority_json(text), "operational authority")
    _exact_fields(raw, PERSISTENT_AUTHORITY_FIELDS, "Persistent authority")
    if raw.get("schema_version") != 2:
        raise AuthorityError("Unsupported or missing operational authority schema_version.")
    if raw.get("authority_file") != "workspace/PROJECT_STATUS.md":
        raise AuthorityError("authority_file must identify workspace/PROJECT_STATUS.md.")
    revision = raw.get("authority_revision")
    if isinstance(revision, bool) or not isinstance(revision, int) or revision <= 0:
        raise AuthorityError("authority_revision must be a positive integer.")

    mission_data = raw.get("authorized_mission")
    if not isinstance(mission_data, dict) or set(mission_data) != {"id", "status", "mode"}:
        raise AuthorityError("authorized_mission must contain exactly id, status, and mode.")
    mission_id = mission_data.get("id")
    status = mission_data.get("status")
    mode = mission_data.get("mode")
    if not isinstance(mission_id, str) or not mission_id.strip():
        raise AuthorityError("authorized_mission.id must be a non-empty string.")
    if not isinstance(status, str) or not status.strip():
        raise AuthorityError("authorized_mission.status must be a non-empty string.")
    if not isinstance(mode, str) or mode not in KNOWN_MODES:
        raise AuthorityError("authorized_mission.mode must be a known mode.")

    _mission_history(raw.get("held_missions"), "held_missions")
    _mission_history(raw.get("completed_missions"), "completed_missions")
    for field, expected in (
        ("m021", "HOLD"),
        ("bounties", "EXPERIMENTAL_HOLD"),
        ("production_deployment", "DEFERRED_NOT_AUTHORIZED"),
    ):
        if raw.get(field) != expected:
            raise AuthorityError(f"{field} must be {expected!r}.")
    allowed = _string_list(raw.get("allowed_actions"), "allowed_actions")
    forbidden = _string_list(raw.get("forbidden_actions"), "forbidden_actions")
    if set(allowed) & set(forbidden):
        raise AuthorityError("An action cannot be both allowed and forbidden.")
    return OperationalAuthority(
        authority_file="workspace/PROJECT_STATUS.md",
        authority_revision=revision,
        mission=AuthorizedMission(mission_id, status, mode, allowed, forbidden),
        raw=raw,
    )


def load_authority(status_file: Path | str = DEFAULT_STATUS_FILE) -> OperationalAuthority:
    """Load the sole persistent operational authority from PROJECT_STATUS.md."""

    path = Path(status_file)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise AuthorityError(f"Cannot read canonical authority file: {path}.") from error
    return parse_authority_text(text)


def _runtime_lease_path(lease_file: Path | str | None) -> Path:
    if lease_file is not None:
        return Path(lease_file)
    return Path(os.environ.get("MELOMANOS_AUTHORITY_LEASE_FILE", DEFAULT_AUTHORITY_LEASE_FILE))


def _validate_lease_location(path: Path) -> None:
    """Reject lease locations inside any repository rather than merely relying on convention."""

    resolved = path.resolve()
    root = DEFAULT_STATUS_FILE.parent.parent.resolve()
    ai_dev_os = Path(os.environ.get("MELOMANOS_AI_DEV_OS_DIR", root / "ai-dev-os")).resolve()
    for repository in (root, ai_dev_os):
        try:
            resolved.relative_to(repository)
        except ValueError:
            continue
        raise AuthorityError("Runtime lease file must be outside all repositories.")


def parse_lease_text(text: str) -> RuntimeLease:
    """Parse and structurally validate an ephemeral runtime lease."""

    raw = _json_object(text, "runtime lease")
    _exact_fields(raw, LEASE_FIELDS, "Runtime lease")
    if raw.get("lease_schema_version") != 1:
        raise AuthorityError("Unsupported or missing runtime lease schema version.")
    lease_id = raw.get("lease_id")
    if not isinstance(lease_id, str) or not lease_id.strip():
        raise AuthorityError("lease_id must be a non-empty string.")
    revision = raw.get("authority_revision")
    if isinstance(revision, bool) or not isinstance(revision, int) or revision <= 0:
        raise AuthorityError("Lease authority_revision must be a positive integer.")
    mission_id = raw.get("mission_id")
    if not isinstance(mission_id, str) or not mission_id.strip():
        raise AuthorityError("mission_id must be a non-empty string.")
    mode = raw.get("mode")
    if not isinstance(mode, str) or mode not in KNOWN_MODES:
        raise AuthorityError("Lease mode must be a known mode.")
    issued_at = _timestamp(raw.get("issued_at_utc"), "issued_at_utc")
    expires_at = _timestamp(raw.get("expires_at_utc"), "expires_at_utc")
    if expires_at <= issued_at:
        raise AuthorityError("expires_at_utc must be later than issued_at_utc.")
    if expires_at - issued_at > MAX_AUTHORITY_LIFETIME:
        raise AuthorityError("Runtime lease validity must not exceed 72 hours.")
    return RuntimeLease(
        lease_id=lease_id,
        authority_revision=revision,
        mission_id=mission_id,
        mode=mode,
        allowed_actions=_string_list(raw.get("allowed_actions"), "lease allowed_actions"),
        issued_at_utc=issued_at,
        expires_at_utc=expires_at,
        expected_heads=_expected_heads(raw.get("expected_heads")),
    )


def load_runtime_lease(lease_file: Path | str | None = None) -> RuntimeLease:
    """Load a runtime lease only from a location outside all repositories."""

    path = _runtime_lease_path(lease_file)
    _validate_lease_location(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise AuthorityError(f"Cannot read runtime authority lease: {path}.") from error
    return parse_lease_text(text)


def _git_dir(repo: Path) -> Path:
    candidate = repo / ".git"
    if candidate.is_dir():
        return candidate
    if candidate.is_file():
        try:
            line = candidate.read_text(encoding="utf-8").strip()
        except OSError as error:
            raise AuthorityError(f"Cannot read Git metadata for {repo}.") from error
        if not line.startswith("gitdir: "):
            raise AuthorityError(f"Malformed Git metadata for {repo}.")
        git_dir = Path(line[len("gitdir: ") :])
        return git_dir if git_dir.is_absolute() else (repo / git_dir).resolve()
    raise AuthorityError(f"Repository metadata not found for {repo}.")


def _git_head(repo: Path) -> str:
    git_dir = _git_dir(repo)
    try:
        head_ref = (git_dir / "HEAD").read_text(encoding="utf-8").strip()
    except OSError as error:
        raise AuthorityError(f"Cannot read Git HEAD for {repo}.") from error
    if head_ref.startswith("ref: "):
        ref_name = head_ref[len("ref: ") :]
        if not ref_name.startswith("refs/"):
            raise AuthorityError(f"Malformed Git HEAD reference for {repo}.")
        ref_path = git_dir / ref_name
        if ref_path.is_file():
            head_ref = ref_path.read_text(encoding="utf-8").strip()
        else:
            try:
                packed = (git_dir / "packed-refs").read_text(encoding="utf-8")
            except OSError as error:
                raise AuthorityError(f"Cannot resolve Git HEAD reference for {repo}.") from error
            matches = [line.split(" ", 1)[0] for line in packed.splitlines() if line.endswith(f" {ref_name}")]
            if len(matches) != 1:
                raise AuthorityError(f"Cannot resolve Git HEAD reference for {repo}.")
            head_ref = matches[0]
    if not HEAD_PATTERN.fullmatch(head_ref):
        raise AuthorityError(f"Malformed Git HEAD for {repo}.")
    return head_ref


def observe_repository_heads(
    repository_paths: Mapping[str, Path | str] | None = None,
) -> dict[str, str]:
    """Read local Git HEAD files without starting a subprocess or touching state."""

    root = DEFAULT_STATUS_FILE.parent.parent
    paths = repository_paths or {
        "workspace": DEFAULT_STATUS_FILE.parent,
        "backend": root / "backend",
        "frontend": root / "frontend",
        "ai_dev_os": Path(os.environ.get("MELOMANOS_AI_DEV_OS_DIR", root / "ai-dev-os")),
    }
    if set(paths) != set(HEAD_NAMES):
        raise AuthorityError("Repository observations must name workspace, backend, frontend, and ai_dev_os.")
    return {name: _git_head(Path(paths[name])) for name in HEAD_NAMES}


def _validated_now(now_utc: datetime | None) -> datetime:
    now = now_utc or datetime.now(UTC)
    if now.tzinfo is None or now.utcoffset() is None:
        raise AuthorityError("Injected current time must be timezone-aware UTC.")
    return now.astimezone(UTC)


def _validate_lease_freshness(lease: RuntimeLease, now_utc: datetime | None) -> None:
    now = _validated_now(now_utc)
    if lease.issued_at_utc > now + MAX_ISSUED_FUTURE_SKEW:
        raise AuthorityError("Runtime lease issued_at_utc is more than five minutes in the future.")
    if lease.expires_at_utc <= now:
        raise AuthorityError("Runtime authority lease has expired.")


def _validate_observed_heads(lease: RuntimeLease, observed_heads: Mapping[str, str] | None) -> None:
    observed = observe_repository_heads() if observed_heads is None else dict(observed_heads)
    if set(observed) != set(HEAD_NAMES):
        raise AuthorityError("Observed HEADs must name workspace, backend, frontend, and ai_dev_os.")
    for name in HEAD_NAMES:
        head = observed[name]
        if not isinstance(head, str) or not HEAD_PATTERN.fullmatch(head):
            raise AuthorityError(f"Observed HEAD for {name} is malformed.")
        if head != lease.expected_heads[name]:
            raise AuthorityError(f"Observed HEAD for {name} does not match runtime lease.")


def _validate_lease_matches_state(authority: OperationalAuthority, lease: RuntimeLease) -> None:
    mission = authority.mission
    if lease.authority_revision != authority.authority_revision:
        raise AuthorityError("Runtime lease authority_revision does not match persistent authority.")
    if lease.mission_id != mission.mission_id:
        raise AuthorityError("Runtime lease mission_id does not match persistent authority.")
    if lease.mode != mission.mode:
        raise AuthorityError("Runtime lease mode does not match persistent authority.")
    if lease.allowed_actions != mission.allowed_actions:
        raise AuthorityError("Runtime lease allowed_actions do not match persistent authority.")


def require_authorized(
    mission_id: str,
    action: str,
    status_file: Path | str = DEFAULT_STATUS_FILE,
    *,
    now_utc: datetime | None = None,
    observed_heads: Mapping[str, str] | None = None,
    lease_file: Path | str | None = None,
) -> OperationalAuthority:
    """Fail closed unless persistent state and a fresh lease permit this action."""

    if not isinstance(mission_id, str) or not mission_id.strip():
        raise AuthorityError("An exact mission ID is required.")
    if not isinstance(action, str) or not action.strip():
        raise AuthorityError("An exact action class is required.")
    if action not in KNOWN_ACTIONS:
        raise AuthorityError(f"Action {action!r} is unknown.")
    authority = load_authority(status_file)
    lease = load_runtime_lease(lease_file)
    _validate_lease_freshness(lease, now_utc)
    _validate_lease_matches_state(authority, lease)
    _validate_observed_heads(lease, observed_heads)
    mission = authority.mission
    if mission.mission_id != mission_id:
        raise AuthorityError(
            f"Mission {mission_id!r} is not the authorized mission {mission.mission_id!r}."
        )
    if mission.status != "READY":
        raise AuthorityError(f"Mission {mission_id!r} is not READY.")
    if action in mission.forbidden_actions:
        raise AuthorityError(f"Action {action!r} is explicitly forbidden.")
    if action not in mission.allowed_actions:
        raise AuthorityError(f"Action {action!r} is not explicitly allowed.")
    return authority


def require_actions(
    mission_id: str,
    actions: tuple[str, ...] | list[str],
    status_file: Path | str = DEFAULT_STATUS_FILE,
    *,
    now_utc: datetime | None = None,
    observed_heads: Mapping[str, str] | None = None,
    lease_file: Path | str | None = None,
) -> OperationalAuthority:
    """Require every requested action before a caller performs any side effect."""

    if not actions:
        raise AuthorityError("At least one exact action class is required.")
    authority: OperationalAuthority | None = None
    for action in actions:
        authority = require_authorized(
            mission_id,
            action,
            status_file,
            now_utc=now_utc,
            observed_heads=observed_heads,
            lease_file=lease_file,
        )
    assert authority is not None
    return authority
