# Limitations

- Model behavior varies by checkpoint, endpoint, serving changes, and sampling.
- Token depth uses a rough four-characters-per-token estimate. It is not exact.
- Offline canned answers validate harness wiring only; they are not model evidence.
- The package test checks current public registry responses, which can change. Network
  failures are recorded as unknown and excluded from the confirmed-name denominator.
- A null control is non-gating; it helps expose baseline behavior but cannot rule out
  every confounder.
- Passing thresholds are project defaults, not universal safety standards.
- A safe model response does not repair an unsafe parser, renderer, tool, or workflow.
- Prompt extraction tests use a synthetic system prompt and cannot establish the
  confidentiality of a production prompt.

Pin the checkpoint and configuration in any report. Re-run surprising results before
making claims about a broader deployment.
