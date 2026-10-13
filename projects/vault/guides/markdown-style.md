# Project documentation writing style

Use simple, formal British English and concise wording. Prefer tables, then lists, then prose where applicable. Explicit document requirements take precedence. Preferences recorded 11 October 2026; refined 13 October 2026.

## Language and length

- Lead with the purpose, outcome or proposed change. Use concrete nouns, precise verbs and consistent terminology.
- Prefer familiar words (`use`, `start`) and active voice when the actor matters. Explain technical terms unfamiliar to the intended reader.
- Keep each paragraph or bullet focused on one connected point. Its sentences should build on one another, with each adding to that point.
- Remove filler, repetition, slang, ornate wording, promotional claims, stock AI phrases, rhetorical questions and forced contrasts. Avoid decorative emphasis and formulaic lists.
- State each point once; repeat only when a standalone summary, procedure or historical checkpoint needs it. End when the useful information is complete; include a next action, owner or deadline when relevant and supplied.
- Preserve facts, conditions, uncertainty, attribution and necessary technical detail. Flag material ambiguity rather than inventing facts or guarantees. Shorter wording must not change meaning or make a proposal sound implemented.

## Document structure

Group related facts, rationale and implications together. Order sections and points so each prepares the reader for the next and advances the document's purpose. For explanations, proposals and design narratives, connect the need, approach, implications and next step; these are a narrative arc, not mandatory headings.

Apply the **whiteboard test**: include only the detail needed to explain the purpose, main parts, responsibilities and flow, or assess key claims and decisions. Explain functions when their roles, inputs/outputs or interactions help understanding; avoid line-by-line code walkthroughs and incidental implementation detail. Prefer stable file/function references; include source line numbers only when essential to locate evidence or perform an action. Link supporting detail that interrupts the explanation.

Specifications, references and procedures retain their required precision and detail; a high-level overview does not replace them.

## Structure and formatting

Prefer formats in this order where they fit the content:

| Priority | Format | Use for |
| --- | --- | --- |
| 1 | Tables | Comparisons, mappings, repeated fields and structured summaries. |
| 2 | Bullet points | Related distinct points; number steps when order matters. |
| 3 | Prose | Connected explanations, reasoning and transitions. |

- Keep list wording parallel and table cells brief. Avoid restating tables in nearby prose.
- Use descriptive headings only where they help navigation. Follow an established document format; omit empty sections and decorative templates.

Example: “It is important to note that the proposed service would retry failed requests” becomes “The proposed service would retry failed requests.” The proposal remains a proposal.

## Current facts and changes

Read the surrounding document and update its maintained account. Preserve frontmatter, code, quotations, identifiers, links and historical checkpoints unless the request targets them. Correct historical facts with dated amendments retaining the original account.

Separate current facts from identified changes. Track each change independently:

| State | Values |
| --- | --- |
| Decision | `proposed`, `accepted`, `rejected`, `superseded` |
| Implementation | `not-started`, `partial`, `implemented`, `not-applicable` (only when no implementation is required) |
| Verification | `not-checked`, `passed`, `failed`, `needs-recheck` |

Record evidence, date, revision, environment and checked scope; mark unknown or stale claims. Acceptance alone changes decision state. Project summaries link to detailed facts rather than duplicating them.

## Sources and media

- Link evidence near the supported claim. Distinguish observation, inference and proposal; use exact commits/paths for historical sources where available.
- Use relative local links and keep existing media paths. New feature assets belong in `features/assets/<feature-id>/`; task-only assets belong in the task's `assets/`. Link reusable media instead of copying it.
- Keep editable diagram sources, including `.tex`, beside rendered SVG/PNG assets. Use Mermaid where the viewer supports it; provide a portable fallback when needed. Describe content in alt text and explain the diagram's purpose nearby. Export alone does not verify viewer rendering.

Before delivery, compare the draft with every supplied fact and open issue. Keep unresolved issues unless new evidence or an explicit instruction resolves or excludes them. Check meaning, status, spelling, scope and links. Run applicable existing checks and report only what was actually checked.
