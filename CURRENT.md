# Current state of Vault

Updated: 13 October 2026. Scope: `/Users/jgray/Documents/vault`, macOS. Original source baseline: `0001181`. See the [skills-removal checkpoint](projects/vault/tasks/remove-skills/context.md) for revised-repository evidence.

Vault stores Markdown documentation and task tools. It packages no skills or installer and does not install global user configuration.

| Capability | Observed state and evidence | Limits |
| --- | --- | --- |
| Documentation maintenance | [AGENTS.md](AGENTS.md) requires the [writing guide](projects/vault/guides/markdown-style.md) before edits and a final draft check. [Earlier guide-revision trials](projects/vault/tasks/external-document-skills/context.md#completion-checkpoint-writing-guide-validation) read it before edits. | Finite samples, not a future/other-host guarantee. Later format/depth rules have not had fresh-agent trials. |
| Project discovery | [Descriptor](projects/vault/PROJECT.md), [catalogue](CATALOG.md), helper and tests. | Sessions need Vault's location and filesystem access. |
| Skills/installation removal | [Change remove-skills](planning/docs-repo-design.md#change-remove-skills): packages, installer and installation-only tests removed. | No Vault user-skill links were found on this Mac; removal did not change global configuration. |
| File metadata | [Accepted design](planning/docs-repo-design.md#change-file-metadata) for optional YAML and safe body-preserving removal. | General parsing/removal and webpage syncing remain unimplemented and unchecked. |
| Task-owned tools | Optional task `tools/` and run/evidence entries. JSON fixture checks counts, input preservation and invalid-input refusal. | Evidence covers that fixture, not a hosted service. |
| Repository checks | 34 unit tests and descriptor/catalogue/supported-link checks passed with Python 3.12.14/PyYAML 6.0.3 on macOS. | Remote URLs, rendering and implementation claims need separate evidence. |
| Integration replay | Offline routing/history, task-tool and media-source checks passed; regression replay omits `.agents`. | Full live workflow/browser runs remain unchecked for this revision; style-only CLI cases are recorded separately. |
| GitHub | [expiracy/vault](https://github.com/expiracy/vault) public, verified 12 October 2026; `master` tracks `origin/master`. | Current documentation/guide publication explicitly authorised 13 October 2026; future automatic updates remain outside scope. |

The [setup task](projects/vault/tasks/setup-remediation/context.md) and [design checkpoints](planning/docs-repo-design.md#design-review-resolutions) preserve earlier Windows/installer/skill scopes and hashes. They do not establish current installation behaviour.

Update observed changes here; keep accepted designs separate from implementation and scoped verification.
