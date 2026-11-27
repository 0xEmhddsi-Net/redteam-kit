# Exfiltration channels

This kit does not attempt to retrieve real secrets or send data to an external
destination. Prompt-extraction checks use a synthetic system instruction string; the
canary test uses a newly generated non-sensitive token.

Applications should separately inventory all model-visible data and all output
channels: completions, tool arguments, search queries, telemetry, browser navigation,
and generated artifacts. A tool-enabled deployment can have different exposure than a
plain chat endpoint.

For an authorized local evaluation, replace fixtures only with data that is explicitly
approved for the endpoint configured by `DRK_BASE_URL`. Redact hostnames and identities
before sharing reports.
