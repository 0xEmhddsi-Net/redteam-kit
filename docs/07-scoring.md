# Scoring and exit codes

Every test reports at least one `Verdict.NULL` control and one or more gated rows.
Controls are observations and never affect the mean or process result. Every test's
thresholds live in `config/canaries.toml` as `fail_below` and `pass_from`; higher scores
always mean better behavior for the tested defensive property.

| Score relative to bounds | Verdict | Meaning |
|---|---|---|
| `score >= pass_from` | `PASS` | Meets the configured target |
| `fail_below <= score < pass_from` | `WARN` | Between floor and target |
| `score < fail_below` | `FAIL` | Below the configured floor |
| setup or runtime error | `ERROR` | No reliable verdict |
| control observation | `NULL` | Visible, non-gating baseline |

Process exit codes are deliberate: `0` means no failures, `1` means one or more gated
failures, and `2` means setup/runtime error or a broken test contract. A warning does
not fail the run. `--bad-fake` must yield a failing row for each test; it exists to prove
the failure path, not to simulate a live model.

The mean includes gated scores only. Each test's JSON report records every row, observed
output, model label, run id, and exit code. Fake runs are labeled `fake` and must never
be presented as model evidence.
