# Contributing

## The contract

Every test file must expose exactly four things:

1. `NAME` — str, stable, snake_case, matches the filename.
2. `build(client, cfg)` — returns the list of cases.
3. `run(case)` — returns a `Row` (see `harness/scoring.py`).
4. `main()` — parses args, loops, writes a report, `sys.exit(report.exit_code)`.

A test missing any of these is not merged.

## Two rules that matter more than style

**Every test has a null case.** If the model ignored the instruction entirely, what
would the score be? If that score can still pass, the test proves nothing.

**Decision rules are strings, not vibes.** `pass_at` and `warn_at` live in
`config/canaries.toml` with a comment explaining the number.

## Adding a play

1. Prose first: add or extend a file in `docs/` with the decision rule.
2. Prompt as a separate file in `prompts/<group>/`.
3. Test that loads it via `promptlib.load()`.
4. `CHANGELOG.md` entry.
5. Prove it fails: run against a model known to be weak on it, or `DRK_FAKE=1` with a
   doctored fake. Screenshot the red run in the PR.

## Style

`ruff check .` and `ruff format .` must pass. Python 3.11+. Line length 100. Type hints
on public functions. No new runtime dependency without a sentence in the PR justifying it.

## Registering a finding

Use `reports/TEMPLATE.md`. A finding needs: severity, affected version/checkpoint,
reproducer run id, the naive consumer it breaks, and a concrete fix. Findings against the
model are interesting; findings against *your parser* are actionable — say which one it is.
