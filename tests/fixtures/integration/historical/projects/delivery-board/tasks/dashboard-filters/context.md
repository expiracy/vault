# Dashboard filter design

Task identifier: `dashboard-filters`.
Requested deliverable: a concise, reviewable design for optional status and date filters, combined with AND, preserving default delivery-list behaviour.
Status: complete (design deliverable).
Maintained design: [dashboard, change dashboard-filters](../../features/dashboard.md#change-dashboard-filters).

## Scope and coordination

Recorded: 11 October 2026. The user assigns `/root` as the sole writer of shared Delivery Board documents for this task. Other agents may contribute through read-only review messages. Work is documentation-only; implementation and commits are outside scope.

The filter extension is distinct from the completed [delivery-list task](../delivery-list/context.md#completion-checkpoint-delivery-list). Preserve that checkpoint and the fixture baseline.

## Completion checkpoint: dashboard-filters

Recorded: 11 October 2026, uncommitted documentation workspace.

Delivered change `dashboard-filters`: optional status and inclusive, independently optional date bounds combined with AND; unchanged default fields and input order; Apply validation, Clear filters, missing-date and empty-result behaviour; a small text flow diagram and review cases. Explicit Apply allows date-range edits before results change. The maintained design and project task index were updated; the historical delivery-list checkpoint was preserved.

Checks: read-only semantic review found no remaining contradiction; `scripts/docs_repo.py --root ROOT check` passed descriptors, catalogue and supported local links. The historical checkpoint's SHA-256 matched its pre-edit value. The text diagram was inspected in source; no application or viewer-rendering checks were run.

The design is ready for review. Decision remains `proposed`, implementation `not-started`, and behaviour verification `not-checked`. Confirm the proposed delivery-date source and calendar meaning during review; the fixture supplies no date contract or runtime implementation. No code was implemented or committed. Next action: review the proposal; implementation requires separate authorisation.
