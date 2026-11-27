# redteam-kit

Repeatable black-hat-shaped test kit for **DeepSeek V4.1 Flash**. Built against the
`deepseek-flash` alias (checkpoint `DeepSeek-V4.1-Flash-1017`), OpenAI-compatible API.

Two halves, deliberately separated:

- **`docs/`** — the threat model and the plays, each with an explicit decision rule.
- **`tests/`** — the plays that can be automated, with pass/fail thresholds and exit codes.

Everything is scored. Nothing here reports "looks fine".

## Why this model

| Property | Value | Consequence for testing |
|---|---|---|
| Context window | 1,048,576 tokens [1] | Instruction smuggling is testable at real RAG depth |
| Max output | 384,000 tokens [2] | Parser attacks get room to be long *and* well-formed |
| Params | 552B MoE, 8B active in / 16B active out [2] | Cheap to run at volume, so `--depths` can be wide |
| Structured outputs / function calling | Supported [2] | Output injection is a live path, not theory |
| Image output | None [2] | It reads screenshots, cannot draw |
| Web search | Host-dependent [2] | Exfil-by-query only where a search tool exists |

## The claim, honestly

Not "100% effective". The effective part is the contract: **every test has a null
case, a decision rule, a threshold, and an exit code.** A green run is evidence, a red
run is a task, and a test that can't fail is a bug.

## Quick start

    git clone <this-repo> && cd deepseek-redteam-kit
    make install
    cp .env.example .env      # add DEEPSEEK_API_KEY
    make fast                 # 3 quick tests, ~2 min
    make full                 # all tests, long-context ones included

Offline:

    make offline              # FakeClient, validates wiring, no key needed

## Commands

| Target | Runs | Typical time |
|---|---|---|
| `make fast` | json, csv, ansi | 2 min |
| `make context` | canary recall at all configured depths | 15–40 min |
| `make recon` | slopsquat package harvest + registry checks | 5 min |
| `make full` | everything, then `make report` | 45 min+ |
| `make report` | merges `reports/*.json` into one markdown verdict | instant |

Exit codes: `0` pass, `1` fail, `2` setup error. Usable as a gate.

## Configuration

Environment (`harness/client.py`):

| Var | Default | Meaning |
|---|---|---|
| `DEEPSEEK_API_KEY` | — | required for live runs |
| `DRK_BASE_URL` | `https://api.deepseek.com/v1` | any compatible endpoint |
| `DRK_MODEL` | `deepseek-flash` | model alias |
| `DRK_RUNS_DIR` | `runs` | raw JSONL transcripts |

Tunables (`config/canaries.toml`): depths, token budget, thresholds, temperature.

Set `DRK_FAKE=1` for the offline client.

## Scope of what you may send

Read `SECURITY.md` before pointing this at a private codebase. Short version: assume
everything sent is retained upstream, so scrub or tokenise before the first run.

## Prompts are data

All model instructions live in `prompts/*.md` and are loaded by name. Changing a test's
wording never requires touching Python. Fork the prompt, bump `CHANGELOG.md`.

## Caveats

See `docs/06-limitations.md`. The load-bearing ones: hallucinated packages are a
supply-chain hole if you install blind; CVE/version claims drift and need lookup; output
injection only matters if a downstream consumer is naive, so test *your* parser, not ours.

## Layout

    docs/       threat model, plays, limitations, scoring semantics
    prompts/    all model-facing text, one file per instruction
    tests/      scored, runnable
    harness/    client, prompt loader, verdict logic
    reports/    generated evidence
    config/     tunables

## License

MIT. Test anything, including commercially.

## References

1. Microsoft Foundry catalog, `FW-DeepSeek-V4.1-Flash` — 1,048,576-token window, MoE. https://ai.azure.com/catalog/models/FW-DeepSeek-V4.1-Flash
2. Alibaba Cloud Model Studio, `deepseek-v4.1-flash` — 552B/8B/16B, 384K output, capability table. https://help.aliyun.com/en/model-studio/deepseek-v4-1-flash
