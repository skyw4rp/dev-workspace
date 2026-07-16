"""Unit tests for persistent authority and runtime leases (stdlib only)."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from governance_authority import (  # noqa: E402
    AUTHORITY_BEGIN,
    AUTHORITY_END,
    AuthorityError,
    require_actions,
    require_authorized,
)


NOW = datetime(2026, 7, 16, 5, 0, tzinfo=timezone.utc)
HEADS = {
    "workspace": "1" * 40,
    "backend": "2" * 40,
    "frontend": "3" * 40,
    "ai_dev_os": "4" * 40,
}


def authority_text(
    mission_id="MEL-UX-001",
    status="READY",
    mode="read_only_audit",
    allowed=None,
    forbidden=None,
    revision=4,
    nested_actions=False,
    extra=None,
):
    payload = {
        "schema_version": 2,
        "authority_file": "workspace/PROJECT_STATUS.md",
        "authority_revision": revision,
        "authorized_mission": {"id": mission_id, "status": status, "mode": mode},
        "held_missions": [],
        "completed_missions": [{"id": "MEL-GOV-001-FINAL", "status": "DONE"}],
        "m021": "HOLD",
        "bounties": "EXPERIMENTAL_HOLD",
        "production_deployment": "DEFERRED_NOT_AUTHORIZED",
        "allowed_actions": allowed or ["read_only_inspection"],
        "forbidden_actions": forbidden
        or ["product_code", "product_tests", "product_build", "server", "network", "deployment"],
    }
    if nested_actions:
        payload["authorized_mission"]["allowed_actions"] = payload.pop("allowed_actions")
        payload["authorized_mission"]["forbidden_actions"] = payload.pop("forbidden_actions")
    if extra:
        payload.update(extra)
    return f"prefix\n{AUTHORITY_BEGIN}\n{json.dumps(payload)}\n{AUTHORITY_END}\nsuffix\n"


def lease_text(
    mission_id="MEL-UX-001",
    mode="read_only_audit",
    allowed=None,
    revision=4,
    issued_at="2026-07-16T04:30:36Z",
    expires_at="2026-07-18T04:30:36Z",
    heads=None,
    lease_id="MEL-UX-001-runtime-1",
    extra=None,
):
    payload = {
        "lease_schema_version": 1,
        "lease_id": lease_id,
        "authority_revision": revision,
        "mission_id": mission_id,
        "mode": mode,
        "allowed_actions": allowed or ["read_only_inspection"],
        "issued_at_utc": issued_at,
        "expires_at_utc": expires_at,
        "expected_heads": heads if heads is not None else HEADS,
    }
    if extra:
        payload.update(extra)
    return json.dumps(payload)


class GovernanceAuthorityTests(unittest.TestCase):
    def fixture(self, text: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "PROJECT_STATUS.md"
        path.write_text(text, encoding="utf-8")
        return path

    def lease_fixture(self, text: str | None = None) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "active-authority-lease.json"
        if text is not None:
            path.write_text(text, encoding="utf-8")
        return path

    def denied(self, text, mission="MEL-UX-001", action="read_only_inspection", *, lease=None, heads=HEADS, now=NOW):
        with self.assertRaises(AuthorityError):
            require_authorized(
                mission,
                action,
                self.fixture(text),
                now_utc=now,
                observed_heads=heads,
                lease_file=self.lease_fixture(lease_text() if lease is None else lease),
            )

    def test_valid_schema_v2_state_and_runtime_lease_pass(self):
        authority = require_authorized(
            "MEL-UX-001",
            "read_only_inspection",
            self.fixture(authority_text()),
            now_utc=NOW,
            observed_heads=HEADS,
            lease_file=self.lease_fixture(lease_text()),
        )
        self.assertEqual(authority.authority_revision, 4)
        self.assertEqual(authority.mission.mode, "read_only_audit")

    def test_persistent_state_contains_no_ephemeral_lease_fields(self):
        payload = json.loads(authority_text().split(AUTHORITY_BEGIN, 1)[1].split(AUTHORITY_END, 1)[0])
        for field in ("authorization_id", "issued_at_utc", "expires_at_utc", "expected_heads", "lease_id"):
            self.assertNotIn(field, payload)

    def test_absent_or_duplicate_authority_block_fails_closed(self):
        self.denied("queue says READY")
        self.denied(authority_text() + authority_text())

    def test_malformed_authority_or_lease_fails_closed(self):
        self.denied(f"{AUTHORITY_BEGIN}\n{{not json}}\n{AUTHORITY_END}")
        self.denied(authority_text(), lease="{not json}")
        self.denied(authority_text(), lease='{"lease_schema_version": 1, "lease_schema_version": 1}')

    def test_missing_lease_fails_closed(self):
        path = self.lease_fixture(None)
        with self.assertRaises(AuthorityError):
            require_authorized("MEL-UX-001", "read_only_inspection", self.fixture(authority_text()), now_utc=NOW, observed_heads=HEADS, lease_file=path)

    def test_invalid_revision_and_legacy_ephemeral_state_fields_fail_closed(self):
        for revision in (0, -1, "4", True):
            with self.subTest(revision=revision):
                self.denied(authority_text(revision=revision))
        self.denied(authority_text(extra={"authorization_id": "legacy"}))

    def test_expired_future_and_overlong_lease_fail_closed(self):
        cases = (
            lease_text(issued_at="2026-07-14T04:30:36Z", expires_at="2026-07-15T04:30:36Z"),
            lease_text(issued_at="2026-07-16T05:05:01Z", expires_at="2026-07-16T06:05:01Z"),
            lease_text(issued_at="2026-07-16T00:00:00Z", expires_at="2026-07-19T00:00:01Z"),
            lease_text(issued_at="2026-07-16 04:30:36"),
        )
        for lease in cases:
            with self.subTest(lease=lease):
                self.denied(authority_text(), lease=lease)

    def test_lease_must_match_persistent_revision_mission_mode_and_actions(self):
        for lease in (
            lease_text(revision=5),
            lease_text(mission_id="M-021"),
            lease_text(mode="governance_only"),
            lease_text(allowed=["governance_docs"]),
        ):
            with self.subTest(lease=lease):
                self.denied(authority_text(), lease=lease)

    def test_invalid_or_unknown_persistent_and_lease_modes_fail_closed(self):
        self.denied(authority_text(mode="unknown_mode"))
        self.denied(authority_text(mode=1))
        self.denied(authority_text(), lease=lease_text(mode="unknown_mode"))
        self.denied(authority_text(), lease=lease_text(extra={"mode": 1}))

    def test_observed_head_mismatch_and_head_change_after_issuance_fail_closed(self):
        changed = dict(HEADS)
        changed["backend"] = "a" * 40
        self.denied(authority_text(), lease=lease_text(), heads=changed)

    def test_missing_or_malformed_lease_head_fails_closed(self):
        missing = dict(HEADS)
        del missing["frontend"]
        self.denied(authority_text(), lease=lease_text(heads=missing))
        malformed = dict(HEADS)
        malformed["frontend"] = "UPPERCASE"
        self.denied(authority_text(), lease=lease_text(heads=malformed))

    def test_nested_action_arrays_remain_rejected(self):
        self.denied(authority_text(nested_actions=True))

    def test_status_action_and_named_non_authorized_requests_fail_closed(self):
        self.denied(authority_text(status="HOLD"))
        self.denied(authority_text(), action="unknown_action")
        self.denied(authority_text(), action="product_code")
        path = self.fixture(authority_text())
        lease = self.lease_fixture(lease_text())
        for mission in ("M-021", "M-010", "Production Deployment", "ARBITRARY-999"):
            with self.subTest(mission=mission), self.assertRaises(AuthorityError):
                require_authorized(mission, "read_only_inspection", path, now_utc=NOW, observed_heads=HEADS, lease_file=lease)

    def test_post_publication_lease_passes_and_replacement_needs_no_repository_rewrite(self):
        published_heads = {name: value * 40 for name, value in zip(HEADS, ("a", "b", "c", "d"))}
        state = self.fixture(authority_text())
        first_lease = self.lease_fixture(lease_text(heads=published_heads, lease_id="issued-after-publication-1"))
        require_authorized("MEL-UX-001", "read_only_inspection", state, now_utc=NOW, observed_heads=published_heads, lease_file=first_lease)
        replacement = self.lease_fixture(lease_text(heads=published_heads, lease_id="issued-after-publication-2"))
        require_authorized("MEL-UX-001", "read_only_inspection", state, now_utc=NOW, observed_heads=published_heads, lease_file=replacement)

    def test_require_actions_accepts_existing_entry_point_shape(self):
        authority = require_actions(
            "MEL-UX-001",
            ("read_only_inspection",),
            self.fixture(authority_text()),
            now_utc=NOW,
            observed_heads=HEADS,
            lease_file=self.lease_fixture(lease_text()),
        )
        self.assertEqual(authority.mission.mission_id, "MEL-UX-001")


if __name__ == "__main__":
    unittest.main()
