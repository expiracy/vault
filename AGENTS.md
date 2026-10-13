# Vault maintenance

Before writing documentation, find and read the existing document that covers the same topic and purpose. Update that document in place by default, integrating new information and correcting or removing outdated statements wherever they appear. Keep its status, evidence, and links consistent with the changes.

Create a new document only when the user explicitly requests one, or when the requested work or an agreed workflow requires a document that has no appropriate existing home. A new finding, changed requirement, or revision is normally an update to an existing document. Do not create dated replacements, numbered copies, or supplemental documents merely to record an update. This rule concerns documents and does not prevent adding supporting images or diagram assets when needed.

Keep proposed behaviour separate from observed current state. An accepted design does not establish that its behaviour is implemented or verified. Preserve material decision history with concise dated notes, supersession links, or existing historical records while keeping the maintained account correct.

## Writing style

Apply the [writing style guide](projects/vault/guides/markdown-style.md) when writing project documents. Follow explicit user instructions for the document.

## Finding context

Vault contains project documents and task tools. It does not package agent skills or install agent configuration. Read `CATALOG.md`, select the relevant `PROJECT.md`, then follow its document and task indexes. Confirm the subject through the descriptor and requested scope before editing. Resume the matching task rather than selecting the newest record. Supply Vault's location through the session or external agent configuration when working from another repository.

## Maintained documents and change states

Reuse the indexed maintained feature or project design for an extension. Keep an appropriate existing document at its current path. When a new feature needs a document with no existing home, the suggested default is `features/<feature-id>.md`. Task records link to that design instead of creating competing copies. Project indexes route to the owning documents; project current-state summaries link to detailed feature facts rather than duplicating them.

Separate observed current design from identified changes. Track each change's decision, implementation, and verification independently. A document containing both current facts and future changes must not have one blanket state applied to all its contents. Record evidence, date, revision, and environment where relevant. When results differ, record implementation and verification per required scope. Overall verification passes only when relevant checks cover the full declared scope; do not narrow that scope without user authorisation. If relevant source or environment facts change, recheck affected claims or mark them as needing recheck.

## Task scope and history

Follow-ups and resumed work reuse the existing task context. Distinct authorised work with new scope can have one new task context under the agreed workflow, while reusing the maintained design. Record the requested deliverable. A design-only task completes by delivering a coherent reviewable design with its status and open issues clear. Implementation follows when requested or already authorised, not merely because the design has been accepted.

Preserve a dated completion checkpoint inside the existing task context: delivered scope, checks and limitations, material decisions and rationale, and relevant requirements or contracts. Link stable change identifiers and, when available, exact docs and code commits with paths. Before Git exists, the checkpoint must preserve the relevant historical facts itself; a mutable link or revision label cannot recover old contents. Keep earlier checkpoints when reopening original task scope. Mark historical errors with dated corrections and retain the original delivery account. Do not rewrite a completed task as though a later extension was included in it.

## Shared edits

Before agents make overlapping edits to a shared design, project summary, index, decision record, or catalogue, one coordinator assigns a single writer. Record the assignment in existing task context and agent instructions. Other agents contribute through their own task records or coordination messages. The writer rereads the document, preserves unrelated edits, reconciles conflicts, and integrates contributions. Coordinate handoffs explicitly. Separate task IDs do not remove this requirement for shared files.

While overlapping work lacks a coordinated writer, keep contributions in task context until the assignment is resolved. This is a cooperation rule, not an automatic filesystem lock.

## Task tools

Vault also holds useful task scripts and small utilities with no suitable home in another repository. Follow the [task tools guide](projects/vault/guides/task-tools.md). Use the existing task context to index source and record the command, working directory, dependencies, inputs/outputs, effects, and scoped checks. Store task-only source in `tasks/<task-id>/tools/`; root `scripts/` remains Vault infrastructure. Reuse and revise appropriate existing tools. Shared tools follow the coordinated-writer rule above.

These local rules implement the requested maintenance policy and reviewed workflow safeguards. The catalogue, helper and project descriptor implement the core layout in [the maintained design](planning/docs-repo-design.md). Check [the current-state record](CURRENT.md) for completed checks and remaining limitations. Instructions do not grant access outside the session's filesystem permissions.
