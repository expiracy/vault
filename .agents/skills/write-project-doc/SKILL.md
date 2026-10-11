---
name: write-project-doc
description: Write or revise Markdown project designs, research notes, guides, and decision records in the central docs repo, preserving existing documents, evidence, change states, and linked media.
---

# Write a project document

Produce the requested reviewable document in its appropriate existing home. A document request or accepted design does not authorise implementation unless the user has also requested it.

## Locate and choose the document

Use `docs_root` from `~/.agents/agent-docs.json` when present. If configuration is absent, resolve this `SKILL.md` through any symlink or junction and use the canonical file's `parents[3]`, the directory above `.agents`. Validate `AGENTS.md` and `CATALOG.md` there and read the central `AGENTS.md` before editing, even from another code repository. Report invalid configuration, missing files, or denied access instead of silently choosing another root. Skills and pointers do not grant filesystem access.

Use the catalogue and relevant `PROJECT.md` index to find the owning document and task. Search and read existing material before writing. Revise the indexed feature or project design for an extension. Create a separate document only when explicitly requested or when authorised work or an agreed workflow needs one with no appropriate existing home. Preserve existing paths and update outdated claims throughout the affected document, rather than adding a conflicting correction at the end.

Before overlapping edits, follow the central coordinated-writer rule. Keep contributions in existing task context until the coordinator assigns the shared document's writer.

## Write and verify

Read [the Markdown style reference](references/markdown-style.md) when composing or substantially revising prose or media. Its British-English defaults are provisional; follow explicit user preferences and refine the reference from actual user feedback.

For maintained designs, distinguish current facts from identified changes and record each change's independent decision, implementation, and verification states. Preserve the change's delta and rationale when integrating checked behaviour. Follow the central scoped-evidence and historical-checkpoint rules; do not present partial checks as full verification or rewrite a completed task to include a later extension.

Check the revised document's links, media paths, evidence, status, and affected index entries. Use the root's Python environment with `scripts/docs_repo.py --root ROOT check`, replacing `ROOT` with the resolved path; prefer `.venv` when present, otherwise Python with PyYAML. Run `catalog --check` when routing metadata changes and regenerate with `catalog` when authorised. These checks establish structural consistency, not the truth of implementation claims. Inspect a diagram or image in the intended viewer when its rendering matters, and state any untested viewer scope.

Record a concise delivery checkpoint in the existing task context and report the document path, requested outcome, relevant checks, and unresolved issues. Complete a design-only task on the design deliverable; leave implementation pending unless separately authorised.
