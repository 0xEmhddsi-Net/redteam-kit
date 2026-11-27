#!/usr/bin/env python3
"""Bury a canary at depth and measure byte-exact recall. Run: python tests/canary_recall.py"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import secrets

from harness import promptlib
from harness.client import make_client
from harness.scoring import Report, Row, Verdict, common_args, decide, errored

NAME = "canary_recall"
CFG = Path("config/canaries.toml")

# Deliberately mundane filler: no numbers, nothing a model likes to "summarise".
FILLER = (
    "The archive shelf was reordered again on Tuesday after the visit, and the clerk "
    "moved the boxes down toward the loading bay because the aisle was narrow. "
) * 12

FAKE_OK = {"Return the canary": "7f3a9c"}
FAKE_BAD = {"Return the canary": "I could not find it."}


def build(client, cfg: dict) -> list[dict]:
    cases = []
    for depth in cfg["depths"]:
        token = f"CNRY{secrets.token_hex(4)}"
        pads = FILLER * max(1, (depth * 4) // len(FILLER)) if depth else ""
        cases.append(
            {
                "depth": depth,
                "token": token,
                "prompt": (
                    f"{pads}\n\nCANARY: {token}\n\n" + promptlib.load("canary/recall")
                    if pads
                    else f"CANARY: {token}\n\n" + promptlib.load("canary/recall")
                ),
            }
        )
    return cases


def run(case: dict, client, cfg: dict) -> Row:
    if not case["depth"]:
        return Row(NAME, "control/depth0", Verdict.NULL, 0.0, "no filler")
    hits = 0
    last = ""
    for _ in range(cfg["trials_per_depth"]):
        last = client.chat(
            case["prompt"], max_tokens=64, temperature=cfg.get("temperature", 0.2)
        ).text
        if case["token"] in last:
            hits += 1
    score = 100.0 * hits / cfg["trials_per_depth"]
    label = f"depth/{case['depth']}"
    return Row(
        NAME,
        label,
        decide(score, cfg["fail_below"], cfg["pass_from"]),
        score,
        f"{hits}/{cfg['trials_per_depth']} exact",
        last[:160],
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    common_args(parser)
    args = parser.parse_args()
    try:
        import tomllib

        cfg = tomllib.loads(CFG
