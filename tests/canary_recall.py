#!/usr/bin/env python3
"""Bury a canary at configured token depths and measure byte-exact recall.

Run: python tests/canary_recall.py
"""

from __future__ import annotations

import argparse
import secrets
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness import promptlib  # noqa: E402
from harness.client import MODEL  # noqa: E402
from harness.scoring import (  # noqa: E402
    Report,
    Row,
    Verdict,
    client_from,
    common_args,
    decide,
    errored,
)

NAME = "canary_recall"
CFG = Path("config/canaries.toml")

FILLER = (
    "The archive shelf was reordered again on Tuesday after the visit, and the clerk "
    "moved the boxes down toward the loading bay because the aisle was narrow. "
) * 12

# Empty: the fake echoes the token itself. Populated: the fake refuses, so --bad-fake fails.
FAKE_OK: dict[str, str] = {}
FAKE_BAD = {"Return the canary": "I could not find it."}


def build(client, cfg: dict) -> list[dict]:
    instruction = promptlib.load("canary/recall")
    cases = []
    for depth in cfg["depths"]:
        token = f"CNRY{secrets.token_hex(4)}"
        if depth:
            pads = FILLER * max(1, (depth * 4) // len(FILLER))
            prompt = f"{pads}\n\nCANARY: {token}\n\n{instruction}"
        else:
            prompt = f"CANARY: {token}\n\n{instruction}"
        cases.append({"depth": depth, "token": token, "prompt": prompt})
    return cases


def run(case: dict, client, cfg: dict) -> Row:
    if not case["depth"]:
        return Row(NAME, "control/depth0", Verdict.NULL, 0.0, "no filler, not gated")

    hits = 0
    last = ""
    for _ in range(cfg["trials_per_depth"]):
        last = client.chat(case["prompt"], max_tokens=64).text
        if case["token"] in last:
            hits += 1

    score = 100.0 * hits / cfg["trials_per_depth"]
    return Row(
        NAME,
        f"depth/{case['depth']}",
        decide(score, cfg["fail_below"], cfg["pass_from"]),
        score,
        f"{hits}/{cfg['trials_per_depth']} exact",
        last[:160],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    common_args(parser)
    args = parser.parse_args()

    report = Report(NAME, MODEL, "unknown")
    try:
        cfg = tomllib.loads(CFG.read_text(encoding="utf-8"))["canary_recall"]
        if args.runs:
            cfg["trials_per_depth"] = args.runs
        client = client_from(args, FAKE_OK, FAKE_BAD)
        report.run_id = client.run_id
        for case in build(client, cfg):
            report.add(run(case, client, cfg))
    except Exception as exc:  # noqa: BLE001 - an ERROR row beats a traceback
        errored(report, "setup", exc)

    report.finish(Path(args.report_dir) / f"{NAME}.json")


if __name__ == "__main__":
    main()
