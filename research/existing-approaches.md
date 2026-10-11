# Existing approaches to shared agent documentation

Researched: 11 October 2026. Scope: a central documentation repository, folders discoverable through descriptions, persistent task context, user review, and Markdown with images and diagrams.

The inspected projects cover useful parts of this idea. The closest precedents are OpenSpec Stores for central planning and Kiro Steering for description-based context selection. A small custom layer looks appropriate for the user's combination of requirements. This is a design judgement, not a claim that no other complete solution exists.

## Agent context and planning

| Approach | Existing behaviour | What to borrow | Fit for this project |
| --- | --- | --- | --- |
| [OpenSpec Stores](https://github.com/Fission-AI/OpenSpec/blob/main/docs/stores-beta/user-guide.md) | A separate Git planning repository can be registered and referenced by multiple code repositories. Reference indexes provide spec summaries and retrieval commands. Stores are beta. | Shared planning plus a small discovery index. | Closest central-repo precedent. Store selection does not grant filesystem access, and synchronisation remains ordinary Git work. |
| [Kiro Steering](https://kiro.dev/docs/steering/) | Context files can carry a name and description and be selected when a request matches that description. | Descriptions that say when context is relevant, followed by selective loading. | Closest precedent for the requested folder descriptions. Its loading behaviour belongs to Kiro and would need an equivalent integration for other agents. |
| [Cline Memory Bank](https://github.com/cline/cline/blob/main/docs/best-practices/memory-bank.mdx) | Markdown files hold project goals, product context, architecture, technical context, active context, and progress. Rules explain when to read and update them. | Separate lasting project knowledge from frequently updated task context. | A useful methodology. Our design should load relevant files selectively as the repository grows. |
| [GitHub Spec Kit](https://github.com/github/spec-kit) | A toolkit of processes, skills, and templates for specification-driven development and other engineering workflows. | Distinguish requirements, design, execution plans, and implementation evidence. | Better suited to a development process than general folder discovery or a personal writing style. |
| [Superpowers](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md) | A brainstorming skill produces written design specifications. A separate [planning skill](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md) produces implementation plans. | Focused skills that leave readable design and planning artifacts. | A precedent for document-producing skills. Its complete workflow is more prescriptive than the current request requires. |

OpenSpec also distinguishes maintained requirements from active change packages containing proposals, designs, tasks, and requirement changes. That separation is valuable when a proposed design must not be mistaken for implemented behaviour. [OpenSpec getting started](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md).

Kiro custom agents require steering resources to be configured explicitly. A portable Markdown file alone does not supply a host's automatic loading behaviour. [Kiro Steering](https://kiro.dev/docs/steering/).

## How an agent would know the repo exists

Codex discovers project instructions along its current project's directory chain. A sibling documentation repository's instructions are not automatically added merely because that repository exists. A small global instruction can point at the central docs location. [Official AGENTS.md guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

Codex supports repository skills and user-scoped skills. Its documented local discovery includes `.agents/skills` within the current repository and the user's `.agents/skills` directory, including symlinked skill folders. A skill stored only in this documentation repository therefore needs a user-scoped installation or another supported distribution mechanism to be discoverable from unrelated projects. [Official skill guidance](https://learn.chatgpt.com/docs/build-skills).

The open Agent Skills format separates discoverable metadata from instructions and supporting resources loaded as needed. That pattern can inspire a project catalogue, but a custom `PROJECT.md` is our own convention and has no automatic loading semantics. [Agent Skills specification](https://agentskills.io/specification).

Discovery and filesystem access are separate requirements. An agent can be told where documents live while still lacking permission to read or edit that location. This session has access to the current documentation workspace. Other sessions must have suitable access configured.

## Document format

Ordinary Markdown meets the chosen review format. GitHub supports relative document and image links, and renders Mermaid diagrams in supported Markdown surfaces. Other viewers can have different capabilities. [Markdown syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax), [diagram support](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams).

Recommendation: keep images beside the document in an `assets/` folder, use relative links, and retain editable diagram sources. Export an SVG or PNG when a diagram must work in a viewer without Mermaid support. No documentation website is needed for the first version.

If review needs change, existing renderers offer optional paths:

- [MkDocs](https://www.mkdocs.org/user-guide/writing-your-docs/) provides a Markdown documentation site and copies local media.
- [MyST](https://mystmd.org/guide/documents-exports) supports richer technical documents and multiple export formats.
- [Quarto](https://quarto.org/docs/reference/formats/) supports website and report output formats.

These are later options rather than dependencies of the proposed repository. A rendering-stack selection would need a fresh check when implementation is requested.

## Decisions and audit

Short architecture decision records provide an established way to preserve a significant decision's context, outcome, status, and consequences. Superseded decisions remain available with links to their replacements. [Michael Nygard's original ADR article](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

For this repo, readable task summaries, links to evidence, and Git history would support user audit. An agent-written progress statement is still a statement to verify, rather than independent proof that work succeeded. The design should record what was checked and which revision was inspected where relevant.

## Existing local resources

Read-only inspection found an existing `report-writing` skill, plus bundled technical-documentation, memory-management, and artifact-template capabilities. The report-writing skill supplies possible prose preferences such as British English, clear sentences, concrete claims, and restrained language. Its LaTeX conventions and report-specific voice rules should not be carried into general Markdown docs without choosing them deliberately.

The bundled memory-management skill uses a compact index backed by deeper files. The technical-documentation skill describes several document types. Artifact templates can preserve reference layouts for formatted documents, but they do not solve central folder discovery.

The workspace was empty and was not a Git repository before these planning notes were created. No tools were installed and no global agent configuration was changed during this research.
