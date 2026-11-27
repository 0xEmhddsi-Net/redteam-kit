"""Verdicts, rows, and exit codes. Every test scores through here or it does not ship."""

from __future__ import annotations

import sys
from dataclasses import asdict, dataclass, field
from enum import Enum

from harness.client import Client


class Verdict(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    ERROR = "error"
    NULL = "null"  # control observation, never gates


@dataclass
class Row:
    test: str
    case: str
    verdict: Verdict
    score: float
    detail: str = ""
    observed: str = ""

    def line(self) -> str:
        mark = {"pass": "PASS", "warn": "WARN", "fail": "FAIL", "error": "ERR", "null": "null"}
        return f"[{mark[self.verdict.value]}] {self.case}  score={self.score:.1f}  {self.detail}"


@dataclass
class Report:
    test: str
    model: str
    run_id: str
    rows: list[Row] = field(default_factory=list)

    def add(self, row: Row) -> None:
        self.rows.append(row)
        print(row.line())

    def gated(self) -> list[Row]:
        return [r for r in self.rows if r.verdict is not Verdict.NULL]

    def scores(self) -> list[float]:
        return [r.score for r in self.gated()]

    def mean(self) -> float:
        gated = self.scores()
        return sum(gated) / len(gated) if gated else 0.0

    @property
    def exit_code(self) -> int:
        if any(r.verdict is Verdict.ERROR for r in self.rows):
            return 2
        return 1 if any(r.verdict is Verdict.FAIL for r in self.rows) else 0

    def payload(self) -> dict:
        return {
            "test": self.test,
            "model": self.model,
            "run_id": self.run_id,
            "mean": round(self.mean(), 2),
            "exit_code": self.exit_code,
            "rows": [asdict(r) for r in self.rows],
        }

    def finish(self, path) -> None:
        import json

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.payload(), indent=2), encoding="utf-8")
        print(f"\n{self.test}: mean {self.mean():.1f} over {len(self.gated())} cases -> {path}")
        sys.exit(self.exit_code)


def decide(score: float, fail_below: float, pass_from: float) -> Verdict:
    """Floor/target judgement. Both bounds are mandatory: a one-sided test is a wish."""
    if score >= pass_from:
        return Verdict.PASS
    if score >= fail_below:
        return Verdict.WARN
    return Verdict.FAIL


def errored(report: Report, name: str, exc: Exception) -> None:
    report.add(Row(name, "setup", Verdict.ERROR, 0.0, f"{type(exc).__name__}: {exc}"))


def common_args(parser) -> None:
    parser.add_argument("--runs", type=int, default=None, help="override config trial count")
    parser.add_argument("--report-dir", default="reports")
    parser.add_argument("--bad-fake", action="store_true", help="use canned failing answers")
    parser.add_argument("--seed", type=int, default=1337)


def client_from(args, fake_ok: dict, fake_bad: dict) -> Client:
    return make_client(fake_bad if args.bad_fake else fake_ok, temperature=0.2)
