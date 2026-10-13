# Existing approaches to shared agent documentation

Researched: 11 October 2026. Scope: a central documentation repo, description-based folder discovery, persistent task context, user review, and Markdown with images and diagrams.

Follow-up decision, 12 October 2026: Vault must not contain skills or a skill installer. The [maintained design](../planning/docs-repo-design.md#change-remove-skills) uses ordinary instructions and guides. The research and local inspection below remain historical.

OpenSpec Stores and Kiro Steering were the closest inspected precedents for central planning and description-based context selection. A small custom layer appeared appropriate for the combined requirements. This design judgement does not exclude other complete solutions.

## Agent context and planning

| Approach | Existing behaviour | What to borrow | Fit for this project |
| --- | --- | --- | --- |
| [OpenSpec Stores](https://github.com/Fission-AI/OpenSpec/blob/main/docs/stores-beta/user-guide.md) | Beta: multiple code repositories reference a registered Git planning repo; indexes give spec summaries and retrieval commands. | Shared planning and a discovery index. | Closest central-repo precedent. Selection grants no filesystem access; synchronisation uses Git. |
| [Kiro Steering](https://kiro.dev/docs/steering/) | Named context files can be selected when requests match their descriptions. | Relevance descriptions and selective loading. | Closest folder-description precedent. Other agents need equivalent loading integration. |
| [Cline Memory Bank](https://github.com/cline/cline/blob/main/docs/best-practices/memory-bank.mdx) | Markdown holds project goals, product context, architecture, technical context, active context and progress, with read/update rules. | Separate lasting knowledge from changing task context. | Useful methodology; load relevant files selectively as the repo grows. |
| [GitHub Spec Kit](https://github.com/github/spec-kit) | Processes, skills and templates for specification-driven development and other engineering workflows. | Separate requirements, design, execution plans and implementation evidence. | Suits development workflows more than folder discovery or personal writing style. |
| [Superpowers](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md) | A brainstorming skill produces design specifications; a [planning skill](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md) produces implementation plans. | Skills that produce readable design and planning artifacts. | Document-producing precedent; its full workflow is more prescriptive than needed. |

OpenSpec separates maintained requirements from active packages of proposals, designs, tasks and requirement changes. This helps distinguish proposals from implemented behaviour. [OpenSpec getting started](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md).

Kiro custom agents require explicit steering-resource configuration; portable Markdown alone cannot provide automatic loading. [Kiro Steering](https://kiro.dev/docs/steering/).

## How an agent would know the repo exists

Codex discovers instructions along the current project's directory chain, without automatically adding a sibling documentation repo. A global instruction can provide its location. [Official AGENTS.md guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

Codex's documented skill discovery includes repository and user `.agents/skills` directories, including symlinked folders. A skill held only in this documentation repo therefore needs user-scoped installation or another supported distribution mechanism for unrelated projects. [Official skill guidance](https://learn.chatgpt.com/docs/build-skills).

The open Agent Skills format separates discoverable metadata from instructions and resources loaded as needed. This can inform a catalogue, but our custom `PROJECT.md` convention provides no automatic loading. [Agent Skills specification](https://agentskills.io/specification).

Discovery does not grant read or write permission. The research session had workspace access; other sessions need suitable access configured.

## Document format

Markdown meets the chosen review format. GitHub supports relative document/image links and Mermaid in supported Markdown surfaces; other viewers may differ. [Markdown syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax), [diagram support](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams).

Recommendation: keep images in a neighbouring `assets/` folder, use relative links, retain editable diagram sources, and export SVG/PNG for viewers without Mermaid. The first version needs no website.

Optional renderers if review needs change:

- [MkDocs](https://www.mkdocs.org/user-guide/writing-your-docs/) provides a Markdown documentation site and copies local media.
- [MyST](https://mystmd.org/guide/documents-exports) supports richer technical documents and multiple export formats.
- [Quarto](https://quarto.org/docs/reference/formats/) supports website and report output formats.

These are later options, not proposed dependencies. Check them afresh before selecting a rendering stack for implementation.

## Decisions and audit

Short architecture decision records preserve significant decisions' context, outcome, status and consequences, retaining superseded decisions with replacement links. [Michael Nygard's original ADR article](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

Task summaries, evidence links and Git history would support user audit. Agent-written progress is not independent proof: record the checks and relevant inspected revision.

## Existing local resources

Read-only inspection found a `report-writing` skill and bundled technical-documentation, memory-management and artifact-template capabilities. The report-writing prose preferences included British English, clear sentences, concrete claims and restrained language. Adopting its LaTeX conventions or report-specific voice for general Markdown would require a deliberate choice.

Memory-management used a compact index backed by deeper files; technical-documentation described several document types. Artifact templates could preserve reference layouts for formatted documents, without solving central folder discovery.

Before these planning notes, the workspace was empty and had no Git repository. This research installed no tools and changed no global agent configuration.
