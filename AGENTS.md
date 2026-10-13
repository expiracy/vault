# Vault maintenance

## Finding context

1. Read `CATALOG.md`, confirm the subject and requested scope in `PROJECT.md`, then follow its document and task indexes.
2. Resume the matching task; do not select the newest record by default.
3. From another repository, supply Vault's location through the session or external configuration. Instructions do not grant filesystem access.

Vault stores project documents and task tools. It does not package skills or install agent configuration.

## Writing style

Before creating or revising any project document, read the [writing guide](projects/vault/guides/markdown-style.md). Apply it and check the draft against it before delivery. Explicit document requirements take precedence.

## Document maintenance

- Read the existing document covering the same topic and purpose. Update it in place, integrating changes and correcting stale statements throughout. Keep status, evidence and links consistent.
- Create a document only when explicitly requested or when authorised work needs one with no suitable existing home. A finding, revision or changed requirement normally updates an existing document. Avoid dated replacements, numbered copies and supplemental update documents; supporting media may be added.
- Separate observed current facts from proposed behaviour. Design acceptance does not prove implementation or verification. Preserve material decisions through dated notes, supersession links or existing history.

## Maintained documents and change states

- Extend the indexed feature or project design at its existing path. For a new feature with no suitable document, prefer `features/<feature-id>.md`; task records link to it. Indexes route to owning documents, and project summaries link to detailed feature facts.
- Keep stable change IDs in section titles and link their originating task. Track decision, implementation and verification independently; mixed current facts and future changes cannot have one blanket state.
- Record evidence, date, revision and environment where relevant. Record implementation and verification per required scope when results differ. Overall verification passes only when checks cover the full declared scope; do not narrow it without user authorisation.
- When relevant source or environment facts change, recheck affected claims or mark them as needing recheck.

## Task scope and history

Reuse task context for follow-ups and resumed work. Distinct authorised scope may have one new context while reusing the maintained design. Record the requested deliverable: design-only work completes with a coherent reviewable design, clear status and open issues. Implementation requires a request or existing authorisation; acceptance alone does not authorise it.

Keep dated completion checkpoints in the task context: delivered scope, checks and limits, material decisions and rationale, requirements/contracts, stable change IDs and exact docs/code commits with paths when available. Before Git exists, preserve the historical facts themselves; mutable links or revision labels cannot recover them. Retain earlier checkpoints when reopening work. Correct historical errors with dated amendments, preserving the original delivery account and keeping later extensions separate.

## Shared edits

Before overlapping edits to shared designs, summaries, indexes, decisions, catalogues or tools, a coordinator assigns one writer and records the assignment in existing task context and agent instructions. Other agents contribute through task records or coordination messages. The writer rereads current content, preserves unrelated changes and reconciles contributions. Explicitly coordinate handoffs; separate task IDs do not remove this requirement.

Until an overlapping edit has a coordinated writer, keep contributions in task context. This is cooperation, not a filesystem lock.

## Task tools

Follow the [task tools guide](projects/vault/guides/task-tools.md) for utilities with no suitable home in another repository. Index source and run instructions in the existing task context, including command, working directory, dependencies, inputs/outputs, effects and scoped checks. Task-only source belongs in `tasks/<task-id>/tools/`; root `scripts/` remains Vault infrastructure.

The [maintained design](planning/docs-repo-design.md) defines the layout and contracts. [CURRENT.md](CURRENT.md) records completed checks and limits.
