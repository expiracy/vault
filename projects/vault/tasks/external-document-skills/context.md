# External document skills

Task: `external-document-skills`. Started and completed after the final clarification: 13 October 2026. Status: complete. Earlier completion checkpoints are retained below.

Requested deliverable, further clarified on 13 October 2026: documentation writing style and LaTeX/TikZ UML diagram assets for Markdown documents. Use the name `uml-diagrams` and keep only sequence, activity, state machine, class, component, deployment and use case views, with explicit scenario-to-view guidance and the existing canonical style. The full LaTeX-document skill created under the earlier interpretation is removed. Keep Vault Markdown and free of packaged skills.

Root is the sole writer of the packages, their skills-index entries, this context and Vault's project-index entry. Canonical source belongs in `/Users/jgray/skills`, now configured as `expiracy/dotfiles`, under `skills/vault-doc-style/` and `skills/uml-diagrams/`. The earlier full-document package is removed. Reuse the existing writing, document and TikZ guidance. Preserve the unrelated chezmoi migration; update only the relevant skill entries, shared instruction reference and matching link templates.

## Original scope and checks

This was the initial interpretation; the diagram-only clarification below supersedes the full-document portion.

- Create one concise `SKILL.md` per skill, with no additional helper scripts or templates.
- Keep Vault's [writing guide](../../guides/markdown-style.md) as the detailed style authority. Preserve custom metadata, change states, links and historical checkpoints during prose edits.
- Cover editable LaTeX source, existing assets, native or available compilation, limited repairs and honest visual-verification reporting. Keep Markdown metadata separate from exported LaTeX prose.
- Validate each manifest and perform isolated document-edit/generation trials before linking the new skills into the existing user skill directory.

## Clarification and current work

The user clarified that LaTeX is for diagrams accompanying Markdown, not full documents, then restricted the skill to common views and requested clear selection guidance. Root preserved `vault-doc-style`, removed the newly created `latex-documents` package and its links/templates, and revised the existing diagram skill before renaming it to `uml-diagrams`. The canonical visual theme is the existing blue/grey palette, typography and line conventions; formal UML notation is checked separately against primary specifications. The unrelated chezmoi migration was subsequently committed outside this task.

The final seven-view manifest passed validation. Examples for all seven retained views compiled and rendered with the trimmed shared theme, and root inspected every PNG. An independent trial selected the intended views, handled an unclear brief and an excluded type, and generated a checked sequence diagram. Installed links resolve to the tested source. Earlier checks of the broader scope remain historical evidence in their checkpoint below.

Current published skill source: [dotfiles commit a144d16](https://github.com/expiracy/dotfiles/commit/a144d1602c5fab71a85d0c1bcf2ce20c9518ed91). The checkpoints below record the original publication and subsequent rename; earlier names and uncommitted states describe those historical deliveries.

## Earlier progress

The writing-style baseline preserved facts but rephrased the historical completion checkpoint. The new skill's trial preserved that checkpoint exactly, as well as metadata, states and links. Its manifest passed validation, and its source was added to the agent skills repository.

The baseline and skill-guided LaTeX documents compiled successfully through the native compiler. Their editor openings were queued in hidden test chats, so visual layout was not checked. Root independently confirmed successful compilation of the skill-guided source. Both manifests passed, and the four selected Codex/Claude links passed chezmoi verification. No creation work remains.

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
