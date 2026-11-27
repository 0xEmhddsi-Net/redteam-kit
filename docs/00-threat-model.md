# Threat model

## Purpose

This kit measures narrow failure modes in a model-facing application: instruction
precedence, untrusted output handling, system-prompt confidentiality, and package-name
grounding. Tests use synthetic text and inert markers. They do not execute model output,
install suggested packages, or contact private services.

## Assets and trust boundaries

| Asset | Boundary | Example failure |
|---|---|---|
| System/developer instructions | Model context | User content is treated as higher priority |
| Retrieved documents and logs | Untrusted input | Embedded instructions are followed |
| Structured output | Model-to-parser boundary | Extra fields or malformed data alter meaning |
| CSV and terminal output | Model-to-renderer boundary | Formula-like cells or control codes mislead a human |
| Package recommendations | Model-to-dependency workflow | Invented names are trusted without registry verification |
| API key and private corpus | Local-to-provider boundary | Prompts or credentials are sent to an unintended endpoint |

## Attacker assumptions

The evaluator can supply crafted, synthetic text to an authorized model endpoint and
observe the response. The attacker does not gain access to the runner, network, secrets,
or a real target. Any deployment-specific exploitability must be assessed separately.

## Out of scope

This is not a penetration-testing framework, exploit launcher, malware generator, or
security certification. It does not execute tools, publish content, install packages,
or test unauthorized systems. The only network lookups are read-only requests to public
package registries in `slopsquat`.

## Decisions

An individual result is evidence about the tested prompt, model checkpoint, and
downstream assumptions. A successful test does not establish general safety. Scores,
controls, limitations, and exit semantics are defined in [07-scoring.md](07-scoring.md).
