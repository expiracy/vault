# Current state of Vault

Updated: 13 October 2026. Scope: `/Users/jgray/Documents/vault` on macOS. The original source baseline is commit `0001181`; verification for the revised repository is recorded in the [remove-skills task](projects/vault/tasks/remove-skills/context.md).

Vault stores project documentation and task tools. Operating and writing guidance is retained as ordinary Markdown. It contains no packaged agent skills or local skill installer and does not change global user configuration.

| Capability | Current state | Evidence and scope |
| --- | --- | --- |
| Documentation maintenance | Rules in `AGENTS.md`; ordinary writing and task-tool guides. | [Writing guide](projects/vault/guides/markdown-style.md), [task tools guide](projects/vault/guides/task-tools.md). Earlier agent exercises remain historical; guide presence does not guarantee automatic compliance. |
| Project discovery | Project descriptors and generated catalogue; the existing helper supports candidate search. | [PROJECT.md](projects/vault/PROJECT.md), [CATALOG.md](CATALOG.md) and helper tests. A session must receive Vault's location and appropriate filesystem access. |
| Skills and installation | Packaged skills, installer and installation-only tests removed. | [Change remove-skills](planning/docs-repo-design.md#change-remove-skills). No Vault user-skill links were found on this Mac; global configuration was not changed. |
| File metadata | Accepted description of optional YAML frontmatter, safe parsing and removal that preserves the body. | [Change file-metadata](planning/docs-repo-design.md#change-file-metadata). General parsing/removal support and webpage syncing are not implemented or checked. |
| Task-owned tools | Optional task `tools/` folders with run instructions and evidence in the owning context. | The retained JSON-count fixture checks counts, input preservation and invalid-input refusal. This covers that fixture rather than a hosted service. |
| Repository checks | Existing catalogue, descriptor and bounded local-link checker retained. | All 34 remaining unit tests passed with Python 3.12.14 and PyYAML 6.0.3 on macOS; descriptors, catalogue and supported local links passed. Remote URLs, rendering and implementation claims require separate evidence. |
| Integration replay | Fixture and harness use ordinary instructions and guides without skill installation. | Offline routing/history, task-tool and media-source checks passed. The regression test replays a checkout without `.agents`. Fresh live-agent and browser runs for this revision have not been performed. |
| GitHub visibility | [expiracy/vault](https://github.com/expiracy/vault) is public, verified on 12 October 2026. | `master` tracks `origin/master`; the user authorised committing and pushing the metadata documentation and skills removal on 13 October 2026. |

Earlier Windows setup, installer and skill checks are preserved in the [setup-remediation context](projects/vault/tasks/setup-remediation/context.md) and the [maintained design's historical checkpoints](planning/docs-repo-design.md#design-review-resolutions). Their input hashes and original scopes remain intact. They do not establish behaviour for the revised repository or a current installation.

Update this record when observed state changes. Keep pending behaviour and accepted designs separate from implementation and scoped verification.
