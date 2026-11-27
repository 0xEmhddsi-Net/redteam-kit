# Offensive toolbar

The tests are small probes, not a general attack workbench. They demonstrate
representative input classes using synthetic records:

- buried instructions and canary recall;
- hostile-looking but inert structured-output content;
- ANSI concealment markers in a sample log;
- requests to disclose a synthetic system prompt;
- unverified package-name suggestions.

There are no tool calls, command payloads, exploit chains, file writes from model
output, package installations, or scans of target hosts. Do not add a play that crosses
those boundaries without a documented authorization model and a separate safety review.

The `--bad-fake` mode is a regression fixture: it deliberately emits failing canned
answers so CI proves that the scoring path can go red. It is not a model result.
