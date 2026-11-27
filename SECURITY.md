# Security notes

## What leaves your machine

Every live run sends prompts to `DRK_BASE_URL`. Treat that host as a third party.

- **Do not paste a private repo unprompted.** Run `slopsquat` and `json_injection` blind;
  run `prompt_extraction` and `canary_recall` only on disposable fixtures.
- **Scrub secrets first.** `gitleaks detect --no-git -v` over anything you intend to send.
- **Tokenise identifiers** if the run is public: rename services, hosts, customer names.

## Credentials

`.env` is gitignored. Keys are read from the environment only, never written to
`runs/`. `make full` will happily burn quota — set a project-level spend cap.

## Determinism

Temperature defaults to `0.2`. Do not raise it for scored tests; you are measuring the
model, not sampling noise. Re-run a red test 3× before filing.

## Reports

`reports/` is committed *cleaned*. Check generated markdown for leaked paths and
internal hostnames before pushing.

## Reporting a kit bug

Open an issue with: test name, seed, run id, the JSONL line numbers, expected vs actual.
A red test with no run id is not reproducible and will be closed.
