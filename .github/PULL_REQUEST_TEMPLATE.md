## What

<!-- one paragraph: the play, the class of bug, the consumer it breaks -->

## Evidence

- Red run id (required for a new test):
- Green run id after fix (if a parser fix is included):
- Model checkpoint tested: `DeepSeek-V4.1-Flash-1017`

## Checklist

- [ ] Null case exists and cannot pass
- [ ] `pass_at` / `warn_at` in `config/canaries.toml`, with a comment
- [ ] Prompt lives in `prompts/`, not in Python
- [ ] `CHANGELOG.md` entry
- [ ] `reports/` output contains no internal hostnames
- [ ] `make lint` clean
