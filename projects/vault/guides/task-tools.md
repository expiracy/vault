# Task tools in Vault

Retain useful task utilities here when they have no suitable home in another repository. Application code and its utilities stay in the owning code repo; root `scripts/` is Vault infrastructure.

## Location and ownership

- Store task-only source in `projects/<project-id>/tasks/<task-id>/tools/`, created only when needed. Reuse the existing context and canonical tool; keep useful deliverables, not every experiment.
- Select the project by subject, including projects without code repos. Do not place unrelated work in the Vault system project. An authorised standalone task can establish a project when it needs a home.
- Link shared source. Move it to `projects/<project-id>/tools/` only when shared ownership warrants it; update current links and preserve historical commit references. Apply the coordinated-writer rule to shared tools.

Optional task entries:

```text
context.md
tools/       Source, tool-specific dependency files and meaningful checks
outputs/     Regenerated results, ignored by default
assets/      Deliberately retained deliverables or fixtures
```

## Discover and run

Follow `CATALOG.md` → `PROJECT.md` → the matching task context. Its **Tools** section owns relative source links and run instructions; no separate tool catalogue, manifest or README per script is required.

| Detail | Record |
| --- | --- |
| Purpose/source | Function and canonical source link. |
| Invocation | Exact command, working directory and available dry-run option. |
| Dependencies | Runtime/packages or dependency-file link; say “standard library only” when applicable. |
| Inputs/outputs | Paths/formats and result location. |
| Effects | Files or external state read/changed; say “none” when applicable. |
| Evidence | Saved, executed or checked; actual checks, date, environment and revision. |

Keep entries brief. Use paths relative to a stated working directory, or resolve resources relative to the script with input/output arguments. Avoid machine-specific maintained commands.

Use existing task authorisation and session permissions. Inspect source when behaviour or effects are unclear. Saving a script or command proves neither execution nor correctness.

## Results and maintenance

Link useful results from context. Keep regenerated output in `outputs/`, deliberate material assets/fixtures in `assets/`, and environments or bulky generated files out of maintained source. Record tool-specific dependencies near the tool rather than in Vault's infrastructure requirements.

After changes, run relevant checks and update the same context with results and limits; recheck affected claims. Preserve the delivered contract and exact source/check revisions in its completion checkpoint.
