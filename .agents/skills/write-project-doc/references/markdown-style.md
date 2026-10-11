# Markdown writing and media

These are provisional defaults drawn from the user's earlier report-writing preferences. The general Markdown style has not yet been agreed through a representative document. Explicit user instructions and feedback take precedence.

## Prose and structure

Use British English, plain words, active sentences, and a restrained tone. State the concrete point early, then develop the evidence or reasoning needed to assess it. Prefer connected paragraphs. Use headings when they help navigation and lists or tables when items are genuinely sequential, parallel, or easier to compare. Avoid forcing a template or adding sections with no useful content.

Explain what changes, why, and how a reader can check it. Name the affected behaviour, interfaces, constraints, trade-offs, and open issues when relevant. Keep implementation details only when they help the document's reader make a decision. Avoid promotional language, vague claims, decorative emphasis, and repeated summaries.

Read the surrounding document before revising it. Integrate the change into its existing account and repair stale references elsewhere. Retain material decision history and completed checkpoints; historical corrections are dated amendments rather than silent rewrites.

## Current facts and changes

In a maintained design, keep **Current design** separate from identified **Change <id>** sections. A section title should preserve the stable change ID. Record the originating task and the substantive change, decision rationale, and relevant evidence.

Track each change independently:

| State | Values |
| --- | --- |
| Decision | `proposed`, `accepted`, `rejected`, `superseded` |
| Implementation | `not-started`, `partial`, `implemented`, `not-applicable` |
| Verification | `not-checked`, `passed`, `failed`, `needs-recheck` |

Design acceptance changes decision state only. Use `not-applicable` only when the change itself needs no implementation, not because the current task is design-only. Record results per required scope when they differ; full verification requires checks covering the full declared scope. Preserve remaining work rather than narrowing the scope to produce a pass.

Support present-state claims with appropriate files, checks, sources, or observations, and their date, revision, and environment. Mark unknown or stale claims clearly. A successful local check does not establish behaviour in another environment. Project current-state summaries link to detailed feature facts; they do not become competing accounts.

## Sources and media

Link evidence near the claim it supports. Distinguish sourced observations from inference or proposed behaviour. Use exact commits and paths for historical references when available, while retaining the task's material delivery account.

Use relative Markdown links for local documents and images. Keep existing media locations; for a new feature document under the suggested layout, use `features/assets/<feature-id>/`, and keep task-only media in that task's `assets/`. Link reusable assets rather than copying them into each task.

Retain editable diagram sources. Mermaid is suitable when the intended viewer supports it; provide an SVG or PNG alternative when needed. An export does not prove that the viewer renders the source diagram. Alt text describes the image's content, and nearby prose explains why it matters. Use visuals to clarify relationships or evidence, rather than decorate the document.
