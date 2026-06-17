"""Parse and advance MVP_ROADMAP.md after a successful release (stdlib only)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from melomanos_paths import (
    BACKEND_STATUS_FILE,
    ROADMAP_FILE,
    WORKSPACE_STATUS_FILE,
)

MARKER_ROADMAP_FOCUS_START = "<!-- STATUS:ROADMAP_FOCUS_START -->"
MARKER_ROADMAP_FOCUS_END = "<!-- STATUS:ROADMAP_FOCUS_END -->"

SECTION_QUEUE = "## Current Priority Queue"
SECTION_ACTIVE = "## Current Active Task"
SECTION_COMPLETED = "## Completed"
SECTION_WORKFLOW = "## Development Workflow"

QUEUE_ITEM_PATTERN = re.compile(
    r"^### (\d+)\. (.+?)\s*$\n(.*?)(?=^### \d+\.|\Z)",
    re.MULTILINE | re.DOTALL,
)
QUEUE_STATUS_PATTERN = re.compile(r"\*\*Status:\*\*\s+(TODO|READY)\b", re.IGNORECASE)
ACTIVE_TASK_PATTERN = re.compile(
    r"## Current Active Task\s*\n+(?:###\s+(.+?)\s*(?:\n|$))",
)
COMPLETED_COUNT_PATTERN = re.compile(
    r"\*\*Status:\*\*\s+\*\*(\d+)\*\*\s+milestones\s+\*\*COMPLETED\*\*",
    re.IGNORECASE,
)
COMPLETED_TABLE_END_PATTERN = re.compile(
    r"(\| \*\*[^|]+\*\* \| ✅ \| ✅ \| [^\n]+\n)\n(\*\*Status:\*\*)",
)
BACKLOG_COMPLETE_STATUS = "Backlog complete / needs planning"

PHASE_PATTERN = re.compile(r"\bphase\b", re.IGNORECASE)
REMAINING_PATTERN = re.compile(r"\*\*Remaining:\*\*", re.IGNORECASE)
SEVEN_PHASES_PATTERN = re.compile(r"\b7\s+phases\b", re.IGNORECASE)
STATUS_IN_PROGRESS_PATTERN = re.compile(
    r"\*\*Status:\*\*\s+IN_PROGRESS\b",
    re.IGNORECASE,
)
UNCHECKED_CHECKBOX_PATTERN = re.compile(r"^\s*[-*]\s*\[\s*\]", re.MULTILINE)

MULTI_PHASE_WARNING = (
    "WARNING: Current active task appears to be a multi-phase epic or still "
    "IN_PROGRESS.\nAuto-advance may be premature."
)


@dataclass
class QueueItem:
    number: int
    title: str
    body: str

    @property
    def status(self) -> str | None:
        match = QUEUE_STATUS_PATTERN.search(self.body)
        return match.group(1).upper() if match else None


@dataclass
class RoadmapAdvancePreview:
    current_task: str | None
    next_task: str | None
    can_advance: bool
    warnings: list[str] = field(default_factory=list)
    backlog_complete: bool = False
    multi_phase_safety: bool = False
    multi_phase_signals: list[str] = field(default_factory=list)


def _normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip()).casefold()


def read_active_task(text: str) -> str | None:
    match = ACTIVE_TASK_PATTERN.search(text)
    if not match:
        return None
    title = match.group(1).strip()
    if title.lower() == "none":
        return None
    return title


def read_active_task_section(text: str) -> str:
    start = text.find(SECTION_ACTIVE)
    if start == -1:
        return ""
    content_start = start + len(SECTION_ACTIVE)
    rest = text[content_start:]
    end_match = re.search(r"\n---\s*\n", rest)
    if end_match:
        return rest[: end_match.start()]
    workflow = rest.find(SECTION_WORKFLOW)
    if workflow != -1:
        return rest[:workflow]
    return rest


def detect_multi_phase_signals(section_text: str) -> list[str]:
    if not section_text.strip():
        return []

    signals: list[str] = []
    if PHASE_PATTERN.search(section_text):
        signals.append("contains 'Phase'")
    if REMAINING_PATTERN.search(section_text):
        signals.append("contains 'Remaining'")
    if SEVEN_PHASES_PATTERN.search(section_text):
        signals.append("contains '7 phases'")
    if STATUS_IN_PROGRESS_PATTERN.search(section_text):
        signals.append("Status is IN_PROGRESS")
    if UNCHECKED_CHECKBOX_PATTERN.search(section_text):
        signals.append("contains unfinished checklist items [ ]")
    return signals


def collect_multi_phase_signals(text: str, current_task: str | None) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []

    def add(signals: list[str]) -> None:
        for signal in signals:
            if signal not in seen:
                seen.add(signal)
                ordered.append(signal)

    add(detect_multi_phase_signals(read_active_task_section(text)))
    if current_task:
        for item in parse_queue_items(text):
            if _normalize_title(item.title) == _normalize_title(current_task):
                add(detect_multi_phase_signals(item.body))
                break
    return ordered


def _extract_section(text: str, start_header: str, end_header: str) -> str | None:
    start = text.find(start_header)
    if start == -1:
        return None
    content_start = start + len(start_header)
    end = text.find(end_header, content_start)
    if end == -1:
        return None
    return text[content_start:end]


def parse_queue_items(text: str) -> list[QueueItem]:
    queue_section = _extract_section(text, SECTION_QUEUE, SECTION_ACTIVE)
    if not queue_section:
        return []
    items: list[QueueItem] = []
    for match in QUEUE_ITEM_PATTERN.finditer(queue_section):
        items.append(
            QueueItem(
                number=int(match.group(1)),
                title=match.group(2).strip(),
                body=match.group(3),
            )
        )
    return items


def preview_roadmap_advance(roadmap_path: Path = ROADMAP_FILE) -> RoadmapAdvancePreview:
    warnings: list[str] = []
    if not roadmap_path.is_file():
        return RoadmapAdvancePreview(
            current_task=None,
            next_task=None,
            can_advance=False,
            warnings=[f"Roadmap not found: {roadmap_path}"],
        )

    text = roadmap_path.read_text(encoding="utf-8")
    current_task = read_active_task(text)
    multi_phase_signals = collect_multi_phase_signals(text, current_task)
    multi_phase_safety = bool(multi_phase_signals)
    if not current_task:
        warnings.append("Current Active Task not detected in MVP_ROADMAP.md")
        return RoadmapAdvancePreview(
            current_task=None,
            next_task=None,
            can_advance=False,
            warnings=warnings,
            multi_phase_safety=multi_phase_safety,
            multi_phase_signals=multi_phase_signals,
        )

    queue_items = parse_queue_items(text)
    if not queue_items:
        warnings.append("Current Priority Queue not detected or empty")
        return RoadmapAdvancePreview(
            current_task=current_task,
            next_task=None,
            can_advance=False,
            warnings=warnings,
            multi_phase_safety=multi_phase_safety,
            multi_phase_signals=multi_phase_signals,
        )

    remaining = [
        item
        for item in queue_items
        if _normalize_title(item.title) != _normalize_title(current_task)
    ]
    eligible = [
        item for item in remaining if item.status in {"TODO", "READY"}
    ]
    if not eligible:
        return RoadmapAdvancePreview(
            current_task=current_task,
            next_task=None,
            can_advance=True,
            backlog_complete=True,
            multi_phase_safety=multi_phase_safety,
            multi_phase_signals=multi_phase_signals,
        )

    return RoadmapAdvancePreview(
        current_task=current_task,
        next_task=eligible[0].title,
        can_advance=True,
        multi_phase_safety=multi_phase_safety,
        multi_phase_signals=multi_phase_signals,
    )


def _renumber_queue_item(item: QueueItem, new_number: int) -> str:
    body = item.body
    if not body.startswith("\n"):
        body = "\n" + body
    return f"### {new_number}. {item.title}{body}"


def _build_queue_section(items: list[QueueItem]) -> str:
    if not items:
        return f"{SECTION_QUEUE}\n\n*(Queue empty — promote items from Future Ideas.)*\n"
    blocks = [_renumber_queue_item(item, index) for index, item in enumerate(items, start=1)]
    return f"{SECTION_QUEUE}\n\n" + "\n---\n\n".join(block.rstrip() + "\n" for block in blocks)


def _build_active_task_section(
    task_title: str | None,
    *,
    backlog_complete: bool = False,
) -> str:
    if backlog_complete or not task_title:
        return f"""{SECTION_ACTIVE}

### None

**Status:** {BACKLOG_COMPLETE_STATUS}

**Next steps:**
1. Review Future Ideas and promote the next milestone into Current Priority Queue.
2. Update roadmap priorities with the team before starting new work.

---"""

    return f"""{SECTION_ACTIVE}

### {task_title}

**Status:** READY

**Next steps:**
1. See **Current Priority Queue** above for goals, dependencies, and tests.
2. Implement backend and frontend per milestone definition.
3. Run Quality Gate (`py -m pytest`, `npm run build`, `npm run test:e2e`).
4. `finish_task.py` → commit → push → update status docs.

---"""


def _add_completed_row(text: str, task_title: str) -> str:
    row = (
        f"| **{task_title}** | ✅ | ✅ | "
        f"Shipped; auto-advanced by finish_task.py |\n"
    )
    if COMPLETED_TABLE_END_PATTERN.search(text):
        return COMPLETED_TABLE_END_PATTERN.sub(rf"\1{row}\n\2", text, count=1)

    completed_start = text.find(SECTION_COMPLETED)
    status_line = text.find("**Status:**", completed_start)
    if completed_start == -1 or status_line == -1:
        raise ValueError("Could not locate Completed table in MVP_ROADMAP.md")
    return text[:status_line] + row + "\n" + text[status_line:]


def _increment_completed_count(text: str) -> str:
    def replacer(match: re.Match[str]) -> str:
        count = int(match.group(1)) + 1
        return match.group(0).replace(match.group(1), str(count), 1)

    updated, count = COMPLETED_COUNT_PATTERN.subn(replacer, text, count=1)
    if count == 0:
        raise ValueError("Could not locate completed milestone count in MVP_ROADMAP.md")
    return updated


def _update_footer(text: str, previous_task: str, next_task: str | None) -> str:
    queue_remaining = len(parse_queue_items(text))
    next_label = next_task or "None (backlog complete)"
    footer = (
        f"*Last updated: {previous_task} completed via finish_task.py; "
        f"active task set to {next_label} "
        f"({queue_remaining} in queue).*"
    )
    if "*Last updated:" in text:
        return re.sub(r"\*Last updated:.*\*", footer, text, count=1)
    return text.rstrip() + "\n\n" + footer + "\n"


def apply_roadmap_advance(
    *,
    roadmap_path: Path = ROADMAP_FILE,
    previous_task: str | None = None,
    force_advance: bool = False,
) -> tuple[str, str | None, bool]:
    """Return (new_roadmap_text, next_task_title, backlog_complete)."""
    if not roadmap_path.is_file():
        raise FileNotFoundError(f"Roadmap not found: {roadmap_path}")

    preview = preview_roadmap_advance(roadmap_path)
    if not preview.can_advance:
        raise ValueError(
            "Roadmap advance blocked: " + "; ".join(preview.warnings or ["unknown error"])
        )
    if preview.multi_phase_safety and not force_advance:
        signal_summary = ", ".join(preview.multi_phase_signals) or "multi-phase signals"
        raise ValueError(
            "Roadmap advance blocked: multi-phase epic safety "
            f"({signal_summary}). Type ADVANCE to confirm or use "
            "--force-advance-roadmap."
        )

    current_task = previous_task or preview.current_task
    if not current_task:
        raise ValueError("Current Active Task not detected; roadmap not modified.")

    text = roadmap_path.read_text(encoding="utf-8")
    if _normalize_title(read_active_task(text) or "") != _normalize_title(current_task):
        raise ValueError(
            f"Roadmap active task mismatch (expected {current_task!r}); not modified."
        )

    queue_items = parse_queue_items(text)
    remaining = [
        item
        for item in queue_items
        if _normalize_title(item.title) != _normalize_title(current_task)
    ]
    eligible = [item for item in remaining if item.status in {"TODO", "READY"}]
    next_task = eligible[0].title if eligible else None
    backlog_complete = next_task is None

    # Avoid duplicate completed rows
    completed_marker = f"| **{current_task}** |"
    if completed_marker not in text:
        text = _add_completed_row(text, current_task)
        text = _increment_completed_count(text)

    new_queue_section = _build_queue_section(remaining)
    queue_start = text.find(SECTION_QUEUE)
    active_start = text.find(SECTION_ACTIVE)
    if queue_start == -1 or active_start == -1:
        raise ValueError("Could not locate roadmap queue/active sections.")

    text = text[:queue_start] + new_queue_section.rstrip() + "\n\n" + text[active_start:]
    active_start = text.find(SECTION_ACTIVE)
    if active_start == -1:
        raise ValueError("Could not relocate Current Active Task section.")

    active_end = text.find("\n---", active_start)
    workflow_start = text.find(SECTION_WORKFLOW, active_start)
    section_end = active_end if active_end != -1 else workflow_start
    if section_end == -1:
        raise ValueError("Could not locate end of Current Active Task section.")

    new_active = _build_active_task_section(
        next_task,
        backlog_complete=backlog_complete,
    )
    text = text[:active_start] + new_active + text[section_end:]
    text = _update_footer(text, current_task, next_task)

    return text, next_task, backlog_complete


def build_roadmap_focus_body(
    *,
    current_task: str | None,
    last_completed: str,
) -> str:
    current_label = current_task or "None"
    return f"""## Roadmap Focus

- **Current Active Task:** {current_label}
- **Last completed task:** {last_completed}"""


def update_workspace_roadmap_focus(
    *,
    current_task: str | None,
    last_completed: str,
    status_path: Path = WORKSPACE_STATUS_FILE,
) -> None:
    if not status_path.is_file():
        raise FileNotFoundError(f"Status file not found: {status_path}")

    body = build_roadmap_focus_body(
        current_task=current_task,
        last_completed=last_completed,
    )
    content = status_path.read_text(encoding="utf-8")

    if (
        MARKER_ROADMAP_FOCUS_START in content
        and MARKER_ROADMAP_FOCUS_END in content
    ):
        start = content.find(MARKER_ROADMAP_FOCUS_START)
        end = content.find(MARKER_ROADMAP_FOCUS_END)
        insert_at = start + len(MARKER_ROADMAP_FOCUS_START)
        content = content[:insert_at] + "\n" + body.rstrip() + "\n" + content[end:]
    else:
        anchor = "<!-- STATUS:LATEST_RELEASE_END -->"
        anchor_at = content.find(anchor)
        if anchor_at == -1:
            content = content.rstrip() + "\n\n"
            content += (
                f"{MARKER_ROADMAP_FOCUS_START}\n{body}\n"
                f"{MARKER_ROADMAP_FOCUS_END}\n"
            )
        else:
            insert_at = anchor_at + len(anchor)
            block = (
                f"\n\n{MARKER_ROADMAP_FOCUS_START}\n{body}\n"
                f"{MARKER_ROADMAP_FOCUS_END}"
            )
            content = content[:insert_at] + block + content[insert_at:]

    status_path.write_text(content, encoding="utf-8", newline="\n")


def update_backend_status_focus(
    *,
    current_task: str | None,
    last_completed: str,
    status_path: Path = BACKEND_STATUS_FILE,
) -> None:
    if not status_path.is_file():
        return

    content = status_path.read_text(encoding="utf-8")
    active_value = current_task or "None"
    status_value = "READY" if current_task else BACKLOG_COMPLETE_STATUS

    content = re.sub(
        r"(\| \*\*Active task\*\* \| ).+? (\|)",
        rf"\1{active_value} \2",
        content,
        count=1,
    )
    content = re.sub(
        r"(\| \*\*Status\*\* \| ).+? (\|)",
        rf"\1{status_value} \2",
        content,
        count=1,
    )
    if "**Last updated:**" in content:
        content = re.sub(
            r"\*\*Last updated:\*\*.*",
            f"**Last updated:** {last_completed} completed; active → {active_value}.",
            content,
            count=1,
        )

    recently = (
        f"### {last_completed}\n\n"
        f"- Auto-advanced by `finish_task.py` after successful release.\n"
        f"- Next active task: **{active_value}**\n"
    )
    recently_pattern = re.compile(
        r"## Recently completed\s*\n+(?:### .+?\n+.*?\n)+",
        re.DOTALL,
    )
    if recently_pattern.search(content):
        content = recently_pattern.sub(
            f"## Recently completed\n\n{recently}\n",
            content,
            count=1,
        )

    status_path.write_text(content, encoding="utf-8", newline="\n")
