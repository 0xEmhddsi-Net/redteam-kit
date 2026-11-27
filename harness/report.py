"""Merge reports/*.json into one markdown verdict."""

from __future__ import annotations

import json
from pathlib import Path

REPORTS = Path("reports")
BAD = {"fail", "error"}


def main() -> int:
    rows: list[dict] = []
    for path in sorted(REPORTS.glob("*.json")):
        try:
            rows.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            print(f"skip unreadable {path}")

    if not rows:
        print("no reports yet")
        return 1

    worst = max(r["exit_code"] for r in rows)
    out = ["# Kit verdict", "", f"Run ids: {', '.join(r['run_id'] for r in rows)}", ""]
    out += ["| Test | Mean | Exit |", "|---|---|---|"]
    out += [f"| {r['test']} | {r['mean']} | {r['exit_code']} |" for r in rows]

    for report in rows:
        reds = [x for x in report["rows"] if x["verdict"] in BAD]
        if reds:
            out += ["", f"## {report['test']} — {len(reds)} red", ""]
            out += [f"- **{x['case']}** ({x['verdict']}): {x['observed'][:400]}" for x in reds]

    target = REPORTS / "VERDICT.md"
    target.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {target}")
    return 1 if worst else 0


if __name__ == "__main__":
    raise SystemExit(main())
