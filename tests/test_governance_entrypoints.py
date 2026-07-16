"""No-side-effect tests for governance guards at executable entry points."""

from __future__ import annotations

import argparse
import sys
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import finish_task  # noqa: E402
import project_status  # noqa: E402
import roadmap_advance  # noqa: E402
from governance_authority import AuthorityError  # noqa: E402


EXPECTED_HEADS = {
    "workspace": "189e9608392dab46e5774bbb68476118cb83d45a",
    "backend": "613331fcb82ed184b46d143df35d256207df799a",
    "frontend": "e8b8564de09ed81d4c1f02839aae34f14e05169d",
    "ai_dev_os": "9140f53dc4ae30112c23971a173c5caa3541a3c8",
}


class GovernanceEntrypointTests(unittest.TestCase):
    def test_finish_task_non_dry_run_denial_stops_all_downstream_work(self):
        args = argparse.Namespace(
            dry_run=False,
            mission_id="MEL-GOV-001-FINAL",
            advance_roadmap=False,
            force_advance_roadmap=False,
            backend_message=None,
            frontend_message=None,
            workspace_message=None,
            skip_backend=False,
            skip_frontend=False,
            skip_workspace=False,
        )
        denial = AuthorityError("non-dry-run actions are not authorized")
        with ExitStack() as stack:
            stack.enter_context(patch.object(finish_task, "parse_args", return_value=args))
            observe_heads = stack.enter_context(
                patch.object(
                    finish_task,
                    "observe_repository_heads",
                    return_value=EXPECTED_HEADS,
                )
            )
            require_actions = stack.enter_context(
                patch.object(
                    finish_task,
                    "require_actions",
                    side_effect=denial,
                )
            )
            active_task = stack.enter_context(
                patch.object(finish_task, "read_active_task_from_roadmap")
            )
            roadmap_plan = stack.enter_context(
                patch.object(finish_task, "plan_roadmap_advance")
            )
            preview_advance = stack.enter_context(
                patch.object(finish_task, "preview_roadmap_advance")
            )
            git_status = stack.enter_context(patch.object(finish_task, "git_status_data"))
            build_repo_state = stack.enter_context(
                patch.object(finish_task, "build_repo_state")
            )
            dry_run_plan = stack.enter_context(
                patch.object(finish_task, "show_dry_run_plan")
            )
            quality_gate = stack.enter_context(
                patch.object(finish_task, "run_quality_gate")
            )
            run_command = stack.enter_context(patch.object(finish_task, "run_command"))
            release_summary = stack.enter_context(
                patch.object(finish_task, "print_release_summary")
            )
            confirm_proceed = stack.enter_context(
                patch.object(finish_task, "confirm_proceed")
            )
            commit_and_push = stack.enter_context(
                patch.object(finish_task, "commit_and_push")
            )
            status_after_release = stack.enter_context(
                patch.object(finish_task, "update_project_status_after_release")
            )
            update_status = stack.enter_context(
                patch.object(finish_task, "update_project_status")
            )
            roadmap_advance = stack.enter_context(
                patch.object(finish_task, "execute_roadmap_advance")
            )
            should_advance = stack.enter_context(
                patch.object(finish_task, "roadmap_should_advance")
            )
            apply_advance = stack.enter_context(
                patch.object(finish_task, "apply_roadmap_advance")
            )
            workspace_focus = stack.enter_context(
                patch.object(finish_task, "update_workspace_roadmap_focus")
            )
            backend_focus = stack.enter_context(
                patch.object(finish_task, "update_backend_status_focus")
            )
            commit_roadmap_docs = stack.enter_context(
                patch.object(finish_task, "commit_roadmap_docs")
            )
            commit_workspace = stack.enter_context(
                patch.object(finish_task, "maybe_commit_workspace")
            )
            suggest_workspace_message = stack.enter_context(
                patch.object(finish_task, "suggest_workspace_message")
            )
            successful_commit = stack.enter_context(
                patch.object(finish_task, "release_had_successful_commit")
            )
            final_summary = stack.enter_context(
                patch.object(finish_task, "print_final_summary")
            )
            subprocess_run = stack.enter_context(
                patch.object(finish_task.subprocess, "run")
            )
            read_text = stack.enter_context(patch.object(Path, "read_text"))
            write_text = stack.enter_context(patch.object(Path, "write_text"))
            print_output = stack.enter_context(patch("builtins.print"))
            with self.assertRaises(SystemExit) as exit_error:
                finish_task.main()

        self.assertEqual(exit_error.exception.code, 1)
        observe_heads.assert_called_once_with()
        require_actions.assert_called_once_with(
            "MEL-GOV-001-FINAL",
            (
                "product_tests",
                "product_build",
                "status_write",
                "roadmap_promotion",
                "stage",
                "commit",
                "push",
            ),
            observed_heads=EXPECTED_HEADS,
        )
        print_output.assert_any_call(
            f"STOP: canonical authority denied finish_task: {denial}"
        )

        for downstream in (
            active_task,
            roadmap_plan,
            preview_advance,
            git_status,
            build_repo_state,
            dry_run_plan,
            quality_gate,
            run_command,
            release_summary,
            confirm_proceed,
            commit_and_push,
            status_after_release,
            update_status,
            roadmap_advance,
            should_advance,
            apply_advance,
            workspace_focus,
            backend_focus,
            commit_roadmap_docs,
            commit_workspace,
            suggest_workspace_message,
            successful_commit,
            final_summary,
            subprocess_run,
            read_text,
            write_text,
        ):
            downstream.assert_not_called()

    def test_finish_task_denial_has_no_downstream_side_effects(self):
        args = argparse.Namespace(
            dry_run=True,
            mission_id="MEL-GOV-001-FINAL",
            advance_roadmap=False,
            force_advance_roadmap=False,
            backend_message=None,
            frontend_message=None,
            workspace_message=None,
            skip_backend=False,
            skip_frontend=False,
            skip_workspace=False,
        )
        with (
            patch.object(finish_task, "parse_args", return_value=args),
            patch.object(finish_task, "observe_repository_heads", return_value=EXPECTED_HEADS),
            patch.object(finish_task, "read_active_task_from_roadmap") as active_task,
            patch.object(finish_task.subprocess, "run") as subprocess_run,
        ):
            with self.assertRaises(SystemExit):
                finish_task.main()
        active_task.assert_not_called()
        subprocess_run.assert_not_called()

    def test_project_status_denial_has_no_status_write(self):
        with (
            patch.object(project_status, "observe_repository_heads", return_value=EXPECTED_HEADS),
            patch.object(Path, "write_text") as write_text,
        ):
            with self.assertRaises(project_status.AuthorityError):
                project_status.update_project_status(
                    mission_id="MEL-GOV-001-FINAL",
                    backend_committed=False,
                    backend_message="",
                    frontend_committed=False,
                    frontend_message="",
                )
        write_text.assert_not_called()

    def test_roadmap_advance_denial_has_no_roadmap_read_or_write(self):
        with (
            patch.object(roadmap_advance, "observe_repository_heads", return_value=EXPECTED_HEADS),
            patch.object(roadmap_advance, "preview_roadmap_advance") as preview,
            patch.object(Path, "write_text") as write_text,
        ):
            with self.assertRaises(AuthorityError):
                roadmap_advance.apply_roadmap_advance(
                    mission_id="MEL-GOV-001-FINAL",
                    roadmap_path=Path("does-not-matter.md"),
                )
        preview.assert_not_called()
        write_text.assert_not_called()


if __name__ == "__main__":
    unittest.main()
