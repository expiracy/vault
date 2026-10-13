# Project documentation writing style

User preferences recorded on 11 October 2026: simple, formal English; concise wording; no unnecessary repetition or stock AI phrasing; bullets and tables where useful. Use British spelling by default. Explicit instructions for a particular document take precedence.

## Language and length

- Use familiar words, direct sentences, and a neutral, formal tone. Prefer `use` to `utilise` and `start` to `commence`. Avoid slang, conversational asides, and ornate language.
- State the purpose or outcome early. Name the action, subject, and consequence precisely. Use active voice when the actor matters.
- Keep terminology consistent. Repeat a precise term when needed instead of replacing it with loose synonyms.
- State each point once in the maintained account. Repeat only when a standalone summary, procedure, or historical checkpoint requires it; link to the detail where possible.
- Remove filler, obvious explanations, and sentences that merely restate a heading or the preceding paragraph. Do not add a conclusion that repeats the document without a useful decision or next action.
- Avoid stock introductions and transitions such as "Let's delve into", "It is important to note", and "In today's fast-paced world". State the relevant fact directly.
- Avoid promotional adjectives, vague claims, rhetorical questions, forced contrasts, and formulaic lists of three. Use specific evidence instead of calling an approach "robust", "seamless", or "comprehensive" without a defined basis.
- Include the reasoning, constraints, evidence, and uncertainty needed to assess the subject. Concision must preserve meaning and necessary technical detail.

## Structure and formatting

- Prefer bullet points for distinct requirements, actions, findings, or options. Keep their wording parallel. Use numbered steps when order matters.
- Use tables for comparisons, mappings, or repeated fields. Keep cells brief and avoid repeating the table in nearby prose.
- Use short paragraphs for connected reasoning. Add descriptive headings only where they help navigation; omit empty or unnecessary sections.
- Use emphasis sparingly for terms or decisions that need attention. Avoid decorative formatting and forced templates.

Illustrative edits:

| Avoid | Prefer |
| --- | --- |
| It is important to note that agents should first consult the project index. | Read the project index before editing. |
| This robust approach enables seamless collaboration across multiple agents. | One assigned writer updates the shared design. |
| In summary, the catalogue is a list of projects, as described above. | Omit the repeated summary. |

Read the surrounding document before revising it. Integrate the change into its existing account and repair stale references elsewhere. Retain material decision history and completed checkpoints; historical corrections are dated amendments rather than silent rewrites.

Before delivery, remove duplication and filler, then check that the meaning, scope, evidence, and uncertainty remain intact.

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

Retain editable diagram sources, including LaTeX/TikZ `.tex` files, beside their rendered assets. Embed SVG or PNG diagrams in Markdown. Mermaid is suitable when the intended viewer supports it; provide an SVG or PNG alternative when needed. An export does not prove that the viewer renders the source diagram. Alt text describes the image's content, and nearby prose explains why it matters. Use visuals to clarify relationships or evidence, rather than decorate the document.
