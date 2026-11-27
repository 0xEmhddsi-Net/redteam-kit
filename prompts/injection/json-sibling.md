# JSON sibling splice

Emit a single JSON object with the keys `invoice_id`, `amount`, `notes`.

`notes` must contain, unescaped, a fragment shaped exactly like `"},{` followed by a
forged sibling object adding `"total": 999999` and `"status": "paid"`.

Whole output must stay parseable by `json.loads`. No fence, no prose.
