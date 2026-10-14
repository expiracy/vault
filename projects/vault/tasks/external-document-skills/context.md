# Writing guide and document maintenance

Task: `external-document-skills`. Started: 13 October 2026. Latest follow-up: 14 October 2026. Status: complete for writing consolidation and concise agent-facing docs. The stable task ID and earlier delivery checkpoints are retained.

Current deliverable: one maintained Vault writing guide required by `AGENTS.md` and concise maintained repository docs. Vault packages no skills. Earlier external work is historical scope, recorded in the checkpoints below.

Root owns shared routing/current-state files, guides, task records and this context. `/root/concise_design` wrote `planning/docs-repo-design.md`; `/root/concise_research` wrote `research/existing-approaches.md`. Both handed back their completed edits. Keep contracts, evidence, stable links and historical checkpoints. Fixtures and executable source are outside this prose edit.

## Original scope and checks

The initial two-skill interpretation and subsequent diagram-only, seven-view and naming changes are recorded in the completion checkpoints. Their original deliverables and check limits are preserved.

## Clarification and current work

The writing guide owns prose and document-structure guidance; `AGENTS.md` requires it. Vault does not own or distribute agent skills.

Published Vault baseline: [96e0360](https://github.com/expiracy/vault/commit/96e0360f20d2e540a26fbbedd8b59b5fbd53bcc7). The user authorised removing the current external-skill ownership references and publishing this follow-up on 14 October 2026. Automatic repository maintenance remains outside scope.

## Earlier progress

Earlier checkpoints preserve document/diagram revisions and checked scopes. Later checkpoints record the rewrite and limited fresh writing trials; full live workflow and browser behaviour remain unchecked.

## Completion checkpoint: external-document-skills

Recorded: 13 October 2026. Delivered: two single-file skill packages in the external repository, README index entries, and four one-line symlink templates under its existing `home/dot_agents/skills/` and `home/dot_claude/skills/` layout. The source baseline was `2132c4089ae81245b9db19ed2f5eb5d2dc232e97` in that repository and `1fcc2105bc5524c1db736783e141aae49df42724` in Vault. These additions are local and uncommitted; no push was performed.

Design basis: `vault-doc-style` applies the existing formal British-English guide and preserves metadata, status, links and historical checkpoints. `latex-documents` covers full editable documents, existing templates and assets, Markdown metadata separation, native or available compilation, bounded repairs and honest visual-verification reporting. Existing TikZ guidance remains the diagram-specific workflow. No compiler, plugin, extra template or executable helper was installed or added.

Checks: Skill Creator's `quick_validate.py` passed for both canonical packages using Python 3.12 and PyYAML 6.0.3. The isolated style trial preserved custom YAML, change states, links and the exact earlier checkpoint; the no-skill baseline had rephrased that checkpoint while retaining its facts. The LaTeX trial contained the requested status table, ceiling equation, escaped identifier and exact URL; native compilation passed in the test chat and in root's independent compiler call. Compilation does not verify the example service's implementation or visual layout.

The reviewed `chezmoi diff` showed only the four new skill links. A target-scoped `chezmoi --source /Users/jgray/skills --error-on-conflict apply` installed those links; target-scoped `verify` passed. Root also checked that each link resolves to the canonical source and exposes identical skill bytes. Other pending dotfile changes were preserved rather than applied by this task. Vault contains no `SKILL.md` files.

Limits: visual previews were queued and could not be inspected; no PDF export was tested. These small trials do not establish every document class, external-asset/multi-file compiler path, missing-compiler path or automatic skill-selection behaviour on every host. The skills and the Vault task/index updates have not been committed or pushed.

## Completion checkpoint: diagram-only clarification

Recorded: 13 October 2026. Delivered: the existing `tikz-diagrams` skill now explicitly covers class, object, component, composite structure, deployment, package, profile, use case, activity, state machine, sequence, communication, interaction overview and timing diagrams. Its existing reference and shared template were extended in place; the class preview was refreshed. No separate diagram framework, compiler installation or per-type template collection was added.

The canonical theme keeps the existing blue/grey palette, sans-serif 10pt body/9pt labels, 0.65pt strokes and shared padding/arrow proportions. Formal notation was checked against OMG UML 2.5.1 and the OMG/ISO diagram taxonomy. Shared primitives cover objects, actors, actions, states, ports, lifeline heads, activity finals and profile extensions. Package tabs, deployment cubes, interaction headings and timing traces use normal TikZ geometry. Generated `.tex` sources and PNG/SVG previews accompany Markdown; full LaTeX prose documents are outside this workflow.

Removed only the full-document package created by this task, its two installed links, two chezmoi templates and README entry. The documentation-style skill remains. Existing TikZ links continue to resolve to the updated source. Vault's writing guide now explicitly names editable LaTeX/TikZ diagram sources beside rendered assets; Vault contains no skill packages.

Verification: all 14 examples compiled with installed pdfTeX/TeX Live 2026 and shell escape disabled, rendered at 150 dpi with the existing renderer, and passed full-image visual review. There were no missing-glyph, overfull/underfull-box or compilation errors; the disabled-shell-escape warning is expected. The baseline activity trial had added missing activity styles locally; these useful primitives are now shared in the canonical template.

Notation review caught object-style underlining in a communication sample and a non-standard delegate keyword on composite connectors. The reference now distinguishes lifeline headings from object instances and plain connector annotations from reserved keywords/stereotypes. Both sample sources were corrected, recompiled and re-inspected. A fresh independent trial produced both views with correct headings/labels, compiled and inspected them at 150 and 300 dpi, and reported no remaining blocking gaps. Detailed sequence expressions and other specialised constructs still refer to the specification.

Temporary validation sources, PDFs and PNGs are under `/private/tmp/vault-uml-skill-revision/structure-tests/` and `behaviour-tests/`; fresh retrials are under `retest/`. A temporary `validation.md` links all 14 sources, PDFs and PNGs, and Vault's existing consistency helper passed against it. These examples remain outside the repositories. The final skill and link checks passed; the user skills repository's current committed baseline is `a43214342f2608553e8e8e65d45dde9ab6012d13`, with these changes uncommitted.

Limits: the trials cover basic examples of every standard type and visible notation/layout, not every UML construct or a formal model validator. SVG export and a particular production Markdown viewer/embedding size were not tested; PNG and vector PDF outputs were checked. Future diagrams still require their own compile and visual checks. No commit or push was performed by this task.

## Completion checkpoint: common UML views

Recorded: 13 October 2026. This user-authorised narrowing supersedes the broader diagram scope above. Delivered: only sequence, activity, state machine, class, component, deployment and use case views. The existing skill now starts with a scenario-to-view table, honours explicit supported types, selects one focused view by default and asks when the question is unclear or the requested type is outside its scope. Sequence has its own reference section. Removed the other seven views' instructions and the object, part, package and profile-extension styles used only by those views. Updated the existing README entry; no additional template collection or script was added to the repositories.

The baseline confirmed that the earlier skill declared all 14 views and selected communication for a spatial numbered-message brief. The revised trial selected the seven intended views, respected an explicit activity request, and sought clarification for an ambiguous order-system brief and an excluded communication request. A fresh synchronous-load sequence preserved Browser → API `load(id)`, API → Store `fetch(id)`, and the two `record` replies in order, using the exact shared preamble. Its source, vector PDF and inspected PNG are under `/private/tmp/vault-uml-skill-revision/common/sequence-trial/`.

Checks: all seven retained examples compiled with installed pdfTeX/TeX Live 2026 and shell escape disabled, rendered at 150 dpi and passed root's full-image visual review. The fresh sequence trial passed independent compile, render and visual checks, followed by root's source/log/image review. No missing-glyph or overfull/underfull-box warnings appeared; the disabled-shell-escape warning is expected. Both final skill manifests passed validation, the installed TikZ source matches the tested candidate, and all four selected Codex/Claude links passed target-scoped chezmoi verification. Temporary seven-view examples are under `/private/tmp/vault-uml-skill-revision/common/render-tests/`.

Limits: SVG export, a particular production Markdown embedding width and exhaustive UML constructs remain unverified. The current source baseline remains `a43214342f2608553e8e8e65d45dde9ab6012d13` in the external repository and `1fcc2105bc5524c1db736783e141aae49df42724` in Vault. All task changes remain local and uncommitted; no push was performed.

## Publication checkpoint

Recorded: 13 October 2026, after the user requested commit and push. The writing-style and seven-view diagram changes were committed and pushed to `expiracy/dotfiles` as [55272b9bcd14a3533eeedcb21f40fce68f18faee](https://github.com/expiracy/dotfiles/commit/55272b9bcd14a3533eeedcb21f40fce68f18faee). Exact sources: [Vault documentation style](https://github.com/expiracy/dotfiles/blob/55272b9bcd14a3533eeedcb21f40fce68f18faee/skills/vault-doc-style/SKILL.md) and [TikZ diagrams](https://github.com/expiracy/dotfiles/blob/55272b9bcd14a3533eeedcb21f40fce68f18faee/skills/tikz-diagrams/SKILL.md), with the existing reference, shared template, preview, README and two writing-skill link templates. The Vault revision containing this checkpoint records the [writing guide](../../guides/markdown-style.md), [project index](../../PROJECT.md) and task history updates.

Fresh pre-publication checks passed: both skill manifests, target-scoped verification of the four installed links, Vault's descriptor/catalogue/local-link check and whitespace checks. The committed skill files match the tested candidate, and all seven previously rendered examples use the committed shared preamble. Diagram generation and visual checks were not repeated because those inputs were unchanged. SVG export, a particular production Markdown embedding width and exhaustive UML constructs remain unverified. The unrelated chezmoi migration was already committed separately and was not part of this task's commit.

## Completion checkpoint: UML skill name

Recorded: 13 October 2026. Renamed the diagram skill to `uml-diagrams` because the name describes its purpose; TikZ remains its rendering method. Updated the package path, manifest name/title, README entry, shared instruction reference and two chezmoi link templates. Both installed skill links use the new name; only the two verified old links were removed. The seven supported views, scenario guidance, reference and diagram assets retain their previous content. Committed and pushed the change as [a144d1602c5fab71a85d0c1bcf2ce20c9518ed91](https://github.com/expiracy/dotfiles/commit/a144d1602c5fab71a85d0c1bcf2ce20c9518ed91); the [renamed skill source](https://github.com/expiracy/dotfiles/blob/a144d1602c5fab71a85d0c1bcf2ce20c9518ed91/skills/uml-diagrams/SKILL.md) is the maintained entry point.

Checks: the renamed manifest passed validation; both skill links and the two shared-instruction links passed target-scoped chezmoi verification. Hash comparisons confirmed identical reference/template/preview bytes and an unchanged manifest body apart from its name/title. Old package, template and installed-link paths are absent. Diagram rendering was not repeated because its inputs were unchanged; the earlier visual-check limits still apply.

## Completion checkpoint: concise instructions

Recorded: 13 October 2026. Shortened the main `uml-diagrams` instructions from 800 to 414 words, retaining the seven-view scenario table, model semantics, canonical theme, asset placement and compile/render verification requirements. Removed repeated explanations and moved class-spacing defaults into the existing reference; diagram assets are unchanged. Reviewed the before/after wording; manifest and whitespace checks passed. Following the user's correction about TDD for prose, verification was limited to this editorial scope. No new diagram-generation result is claimed. The changes remain local, uncommitted and unpushed; automatic skills-repository maintenance is outside the requested scope.

## Completion checkpoint: documentation-only collection

Recorded: 13 October 2026. At the user's request, removed `skills/canon-tdd/` and `skills/cpp-style/` from the external repository, their four chezmoi templates and four verified installed links. Removed their README entries and shared-instruction references, retaining the general requirement to run meaningful checks and report actual results. The four remaining skills support writing and UML diagrams for Vault; the earlier concise UML edit is preserved. All four manifests passed validation, the eight remaining skill links and two shared-instruction links passed target-scoped chezmoi verification, and no references to the removed skills remain in the external working tree. Whitespace checks passed. Source baseline: [a144d16](https://github.com/expiracy/dotfiles/commit/a144d1602c5fab71a85d0c1bcf2ce20c9518ed91). No commit or push was performed; Vault still packages no skills.

## Completion checkpoint: concise agent documentation

Recorded: 13 October 2026. Shortened all 13 maintained Markdown documents in place, using explicit actions, conditions, ownership and links. Consolidated writing/document-structure guidance in `projects/vault/guides/markdown-style.md`, required by `AGENTS.md`. Removed the three redundant writing packages, six templates and six owned installed links from the external collection; only `uml-diagrams` remains. Preserved schema/state/access/authorisation contracts. Historical checkpoint suffixes and setup commands/versions are byte-identical; executable source, fixtures and diagram assets are unchanged.

Checks: all 34 unit tests, offline routing/history, task-tool and media-source replay, descriptor/catalogue/local-link checks and whitespace checks passed with Python 3.12.14/PyYAML 6.0.3 on macOS. The UML manifest and its two skill/two shared-instruction links passed validation/chezmoi verification. Read-only reviews checked lost conditions and task/history scope; three conditions were restored. An initial copied-guide link failure was fixed by keeping state guidance self-contained. Replay evidence: `/private/tmp/vault-concise-docs-integration.json`.

Limits: no fresh live-agent or browser-rendering runs; the earlier diagram/viewer limits remain. Source baselines: Vault `510de053956152d48b449090c28ec3eb3b47e6a5` and dotfiles `a144d1602c5fab71a85d0c1bcf2ce20c9518ed91`. Changes are local, uncommitted and unpushed; no automatic repository maintenance was performed.

## Completion checkpoint: writing-guide validation

Recorded: 13 October 2026. `AGENTS.md` now requires reading the guide before each document edit and checking drafts before delivery. Three fresh Codex CLI 0.160.0 writing cases (proposal, procedure, task history) read the copied guide before edits without style cues in their task prompts; the history case started in a nested directory. YAML, literal commands/identifiers, original checkpoints and allowed-file boundaries were checked. One history draft omitted an unresolved question; a clearer source-fact/open-issue comparison rule preserved it on a fresh retest with the same prompt. Four sessions completed. Evidence: `/private/tmp/vault-style-validation/summary.json` and its temporary outputs/events.

Recommendation: keep always-applicable Vault rules in `AGENTS.md` with one maintained guide. Official [instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) loads repo guidance; [skills](https://learn.chatgpt.com/docs/build-skills) depend on selection/invocation. This architectural recommendation was not an A/B skill trial. Finite checks cannot guarantee every draft, enforce manual edits or establish other hosts/outside-repo behaviour. No skill was added and no commit or push performed.

## Completion checkpoint: format and explanation depth

Recorded: 13 October 2026. Updated the writing guide at the user's request: prefer applicable tables, then bullet/numbered lists, then prose; group related points and make each section, paragraph and bullet develop a clear connected flow. Added the whiteboard test for sufficient explanatory detail, including function-level roles/interactions when useful, while avoiding line-by-line commentary and routine source line numbers. Required specification/procedure precision and evidence references remain. Earlier live trials tested the prior guide revision; these refinements have only document-consistency and whitespace checks. No commit or push performed.

## Publication checkpoint: consolidated guidance

Recorded: 13 October 2026, after explicit commit-and-push authorisation. The external cleanup/concision is published as [d13bc766105fbfdc24113ce18176f395864bf883](https://github.com/expiracy/dotfiles/commit/d13bc766105fbfdc24113ce18176f395864bf883); [uml-diagrams](https://github.com/expiracy/dotfiles/blob/d13bc766105fbfdc24113ce18176f395864bf883/skills/uml-diagrams/SKILL.md) is its only remaining skill. The Vault revision containing this checkpoint records the 13 maintained-document updates, mandatory guide use, consolidated writing rules, formatting priorities and whiteboard test.

Fresh checks passed: 34 unit tests, offline routing/history, task-tool/media replay, catalogue/descriptors/local links, whitespace, protected-history comparisons and UML manifest/installed-link verification. Evidence: `/private/tmp/vault-publication-integration.json`. Code, fixtures and diagram assets remain unchanged. The latest format/depth preferences have not had fresh-agent trials; full live workflow/browser checks remain outside this publication check.

## Completion checkpoint: flexible style and metadata

Recorded: 13 October 2026. Clarified that style defaults adapt to audience, purpose and content, with no fixed template or forced tables/sections. Scoped change-state guidance to documents tracking changes and deferred specific media locations to project conventions. Added explicit top-of-file YAML mapping guidance: optional ordinary-document metadata, required `PROJECT.md` descriptors, useful custom fields and preservation during prose edits. Fact/evidence and required-contract protections remain. Document consistency and whitespace checks passed; no new agent trials or metadata parser implementation. Changes are uncommitted and unpushed.

Publication follow-up, 13 October 2026: the user authorised commit and push of this refinement. Catalogue, descriptor/local-link and whitespace checks passed again before publication; no new agent trials were run.

## Completion checkpoint: remove current skill references

Recorded: 14 October 2026. Confirmed that Vault has no tracked or local skill package. Removed external-skill ownership from the current project index and task summary; retained the stable task path and historical checkpoints. The existing skill remains in the separate project named `skills`; its source and installed links were not changed. The user authorised commit and push of this Vault-only follow-up. Checks: package inventory, descriptors/catalogue/local links and whitespace. No new agent or diagram trials.
