# redteam-kit

Repeatable black-hat-shaped test kit for **DeepSeek V4.1 Flash** (`deepseek-flash`,
checkpoint `DeepSeek-V4.1-Flash-1017`), OpenAI-compatible endpoints.

- **`docs/`** — threat model, plays, limitations, scoring semantics.
- **`tests/`** — the automatable subset, scored, with exit codes.

Every test carries a null control, a floor and a target. A green run is evidence, a red
run is a task, and a test that cannot fail is a bug.

## Why this model

| Property | Value | Consequence |
|---|---|---|
| Context window | 1,048,576 tokens [1] | Instruction smuggling is testable at real RAG depth |
| Max output | 384,000 tokens [2] | Parser attacks get room to be long *and* well-formed |
| MoE 552B, 8B in / 16B out active [2] | voices "Flash" = serving cost | Cheap enough to sweep depths at volume |
| Structured outputs + function calling [2] | supported | Output injection is a live path |
| Image output | none [2] | Reads screenshots, cannot draw |
| Web search | host-dependent [2] | Exfil-by-query only where a search tool exists |

## Install

    python -m venv .venv && . .venv/bin/activate     # Windows: .venv\Scripts\activate
    make install
    cp .env.example .env                              # add DEEPSEEK_API_KEY

Offline, no key:

    make offline

## Commands

| Target | Does | Needs key |
|---|---|---|
| `make offline` | every test with canned answers and no external registry calls | no |
| `make demo` | fast tests + report from an offline run | no |
| `make fast` | json, csv, ansi | yes |
| `make context` | canary recall + prompt-extraction checks | yes |
| `make recon` | package harvest + public registry lookups | yes |
| `make full` | `fast` + `context` + `recon` + report | yes |
| `make lint` / `make compile` | ruff, bytecode check | no |
| `make todo` | list still-unwritten tests | no |

Exit codes: `0` pass, `1` fail, `2` setup error.

## Configuration

| Var | Default | Meaning |
|---|---|---|
| `DEEPSEEK_API_KEY` | — | required live |
| `DRK_BASE_URL` | `https://api.deepseek.com/v1` | any compatible endpoint |
| `DRK_MODEL` | `deepseek-flash` | alias |
| `DRK_RUNS_DIR` | `runs` | transcripts, gitignored |
| `DRK_FAKE` | `0` | `1` = canned client |
| `DRK_TIMEOUT` | `1200` | seconds |

Thresholds are in `config/canaries.toml`. Prompts are files in `prompts/`, loaded by name
— retuning wording never touches Python.

Read `SECURITY.md` before pointing this at anything private. See `docs/06-limitations.md`
for the standing caveats.

## Layout

    docs/       plays and rules        prompts/   model-facing text
    tests/      scored, runnable       harness/   client, scoring, reporting
    config/     tunables               reports/   generated evidence
    fixtures/   your sample corpora

## References

1. Microsoft Foundry, `FW-DeepSeek-V4.1-Flash` — 1,048,576-token window, MoE. https://ai.azure.com/catalog/models/FW-DeepSeek-V4.1-Flash
2. Alibaba Cloud Model Studio, `deepseek-v4.1-flash` — 552B total / 8B in / 16B out active, 384K max output, capability table. https://help.aliyun.com/en/model-studio/deepseek-v4-1-flash

MIT licensed. Test anything, including commercially.
