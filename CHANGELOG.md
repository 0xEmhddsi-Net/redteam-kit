# Changelog

## [0.2.0] — 2026-11-27

### Added
- `json_injection`, `csv_injection`, `ansi_conceal`, `prompt_extraction`, `slopsquat`.
- Null controls on all six tests; `--bad-fake` on every one.
- `docs/07-scoring.md`; threat model through limitations in `docs/00`–`06`.
- `harness/registry.py`, `harness/report.py`, `make demo`, `make todo`.

### Changed
- Threshold keys to `fail_below` / `pass_from`; higher is always better.
- CI compiles before running and gates on both offline and forced-red paths.
- Output-injection fixtures are synthetic and inert; no model output is executed.

### Fixed
- Live client response recording and missing-key setup errors.
- Truncated `tests/canary_recall.py`.

## [0.1.0] — 2026-11-27

### Added
- Initial scaffold, client, scoring, canary recall.
