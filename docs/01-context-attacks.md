# Context attacks

## Buried canary recall

`canary_recall` places a random, synthetic token at configured approximate token depths,
then asks the model to return it exactly. Depth zero is a null control and does not gate.
The score is exact matches divided by trials. Both configured bounds apply to every
non-control depth.

This measures retrieval under long-context load, not whether arbitrary user instructions
should override system policy. Use only a compatible endpoint with a context limit that
can accommodate the configured prompt; reduce depths when the endpoint has a smaller
window. Token depth is estimated from character count and is not tokenizer-calibrated.

## Fixture discipline

Use synthetic or explicitly approved corpora. Do not put credentials, customer records,
or production system prompts in a fixture. A canary is a random test marker, not a secret
management mechanism.
