---
name: docs-context
description: Find central project documentation and recover or update task context when starting or resuming project work, looking up decisions, designing changes, or recording progress.
---

# Central project context

Use the shared documentation repository to find relevant prior work and leave a reviewable checkpoint. Finding documentation does not change the user's requested deliverable or authorise additional implementation.

## Locate the repository

Read `~/.agents/agent-docs.json` when present and use its `docs_root` value. If that configuration is absent, resolve this `SKILL.md` through any symlink or junction and use the canonical file's `parents[3]`: the directory above `.agents`. Do not derive the root from the current code checkout or the unresolved user skill link.

Confirm that the selected root contains `AGENTS.md` and `CATALOG.md`. Read its `AGENTS.md` before any documentation edits, including when working from another repository. If configuration is invalid, required files are missing, or filesystem access is denied, report the specific problem; do not silently create a substitute repository or claim cross-project integration works. Instructions and installed skills do not grant filesystem permissions. Continue independent authorised work where possible.

## Find the owning documents

Read `CATALOG.md` and select candidates using descriptions, names, aliases, and repository identity. Open the relevant `PROJECT.md` to confirm the match, then follow its feature/document and task index. Load only the designs and context needed for the request. If selection remains ambiguous, inspect the candidate descriptors and clarify the scope before writing.

Resume the existing task when the request is a follow-up, handoff, or continuation. Match its requested deliverable and scope rather than choosing the newest task. Search the selected project for an appropriate existing document before creating anything. A new session or message is not a new task. Distinct authorised work can have one new task context under the agreed workflow, while reusing the maintained feature or project design.

When useful, run the helper at `scripts/docs_repo.py` under the selected root. Prefer that root's `.venv/Scripts/python.exe` on Windows or `.venv/bin/python` elsewhere; otherwise use Python with PyYAML installed. Pass `--root` and the resolved root before the subcommand:

- `find QUERY --repository ID` returns candidate project descriptor paths; the repository filter is optional. Select tasks from the descriptor and context, not from this command.
- `catalog --check` checks whether the generated catalogue matches project descriptors.
- `check` checks descriptors and local document/media links.

Use `--help` if the helper interface differs. A stale catalogue is a routing problem: inspect canonical descriptors before relying on its entries. Regenerate with `catalog` only as part of authorised changes and after coordinating any overlapping catalogue edits. Missing runtime dependencies do not prevent reading existing Markdown.

## Recover and checkpoint

Read the relevant maintained design and task context. Recheck source facts needed for the next action; a recent timestamp or accepted design is not verification of current behaviour. Keep observed facts, proposed changes, and scoped implementation/check results distinct.

Update the existing context at meaningful findings, changed scope, completed phases, and handoffs. Record the requested deliverable, status, evidence and applicable date/revision/environment, unresolved issues, and next action. Keep detailed feature truth in its owning maintained design; project summaries and indexes link to it.

Follow the central maintenance, history, and shared-writer rules. Preserve earlier completion checkpoints, stable change IDs, and exact document/code commits where available. Before Git exists, preserve the material historical facts in the checkpoint itself. Mark corrections with dated amendments. Assess completion against the requested deliverable: a design-only task can complete while implementation remains pending.
