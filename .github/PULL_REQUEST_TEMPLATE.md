## What

<!-- the play, the bug class, the naive consumer it breaks -->

## Evidence

- Green run id:
- Red run id (`--bad-fake`):
- Checkpoint: `DeepSeek-V4.1-Flash-1017`

## Checklist

- [ ] `Verdict.NULL` control present and non-gating
- [ ] Both bounds set, commented, higher = better
- [ ] Prompt under `prompts/`, loaded by name
- [ ] `--bad-fake` goes red, proven in this PR
- [ ] `CHANGELOG.md` entry
- [ ] `make lint` and `make compile` clean
- [ ] `reports/` output contains no internal hostnames
