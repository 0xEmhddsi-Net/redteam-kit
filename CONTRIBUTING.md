# Contributing

## The contract — a test missing any of these is not merged

1. `NAME` — str, snake_case, matches the filename.
2. `build(client, cfg)` — returns the case list.
3. `run(case, client, cfg)` — returns a `Row`.
4. `main()` — args, loop, report, and explicit process exit code.
5. One `Verdict.NULL` case that is visible and non-gating.

## Two rules above style

**Every test has a null control.** Ask: if the model ignored the instruction entirely,
what would the score be? The control is informative but cannot determine the verdict.

**Bounds live in config, with a comment.** `fail_below` and `pass_from` are mandatory.
Higher must mean better for the tested defensive property.

## Adding a play

1. Prose first, in `docs/`, including the decision rule.
2. Prompt as its own file under `prompts/<group>/`.
3. Test loads it with `promptlib.load("group/name")`.
4. Prove the failure path with `--bad-fake`; prove a live green result before claiming
   model evidence.
5. Add a `CHANGELOG.md` entry.

## Style

Python 3.11+, line length 100, type hints on public functions. `make lint` clean.
No new runtime dependency without a justification sentence in the PR.

## Findings

Use `reports/TEMPLATE.md`. A finding needs severity, checkpoint, reproducer run id, the
naive consumer it breaks, and a fix. Say explicitly whether the model or your parser is
at fault — the second is the actionable one.
