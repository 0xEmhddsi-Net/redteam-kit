"""Minimal OpenAI-compatible client with JSONL run recording.

Never imports a vendor SDK: the endpoint is a URL, the payload is JSON, and the
transcript is the evidence.
"""

from __future__ import annotations

import json
import os
import re
import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

import httpx

BASE_URL = os.environ.get("DRK_BASE_URL", "https://api.deepseek.com/v1")
MODEL = os.environ.get("DRK_MODEL", "deepseek-flash")
RUNS_DIR = Path(os.environ.get("DRK_RUNS_DIR", "runs"))
TIMEOUT = float(os.environ.get("DRK_TIMEOUT", "1200"))
FAKE = os.environ.get("DRK_FAKE") == "1"

RETRY_STATUS = {408, 429, 500, 502, 503, 504}


@dataclass
class Turn:
    """One round trip, already recorded."""

    text: str
    usage: dict = field(default_factory=dict)
    latency_s: float = 0.0


class Client:
    """Live client. Records every call to RUNS_DIR/<run_id>.jsonl."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = BASE_URL,
        model: str = MODEL,
        temperature: float = 0.2,
        run_id: str | None = None,
        retries: int = 4,
    ) -> None:
        key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        if not key:
            raise ValueError("DEEPSEEK_API_KEY is not set (use DRK_FAKE=1 for offline)")
        self.api_key = key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.retries = retries
        self.run_id = run_id or f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:6]}"
        RUNS_DIR.mkdir(parents=True, exist_ok=True)
        self.ledger = RUNS_DIR / f"{self.run_id}.jsonl"

    def _record(self, record: dict) -> None:
        with self.ledger.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    def chat(
        self,
        prompt: str,
        system: str | None = None,
        max_tokens: int | None = None,
        response_format: dict | None = None,
    ) -> Turn:
        messages: list[dict] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload: dict = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens
        if response_format:
            payload["response_format"] = response_format

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        last_error = "unknown"
        for attempt in range(self.retries + 1):
            started = time.monotonic()
            try:
                with httpx.Client(timeout=TIMEOUT) as http:
                    response = http.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload,
                    )
                if response.status_code in RETRY_STATUS:
                    last_error = f"HTTP {response.status_code}"
                    if attempt < self.retries:
                        time.sleep(min(2**attempt * 2, 60))
                    continue
                response.raise_for_status()
                body = response.json()
                text = body["choices"][0]["message"].get("content") or ""
                usage = body.get("usage", {})
                latency = time.monotonic() - started
                self._record(
                    {
                        "run_id": self.run_id,
                        "ts": datetime.now(UTC).isoformat(),
                        "model": self.model,
                        "payload": payload,
                        "text": text,
                        "usage": usage,
                        "latency_s": round(latency, 3),
                        "attempt": attempt,
                    }
                )
                return Turn(text=text, usage=usage, latency_s=latency)
            except (httpx.HTTPError, KeyError, ValueError, IndexError) as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                if attempt < self.retries:
                    time.sleep(min(2**attempt * 2, 60))

        raise RuntimeError(f"chat failed after {self.retries + 1} attempts: {last_error}")


class FakeClient:
    """Offline stand-in: deterministic, instant, no key.

    Round-trips nothing to disk and claims nothing. It exists so CI can prove the
    wiring and the scoring path, not so it can stand in for evidence.
    """

    run_id = "fake"
    model = "fake"

    def __init__(self, answers: dict[str, str] | None = None) -> None:
        self.answers = answers or {}
        self.calls: list[dict] = []

    def chat(
        self,
        prompt: str,
        system: str | None = None,
        max_tokens: int | None = None,
        response_format: dict | None = None,
    ) -> Turn:
        self.calls.append({"prompt": prompt, "system": system})
        for needle, answer in self.answers.items():
            if needle in prompt:
                return Turn(text=answer)
        if "Return the canary token" in prompt:
            found = re.search(r"CANARY:\s*(\S+)", prompt)
            if found:
                return Turn(text=found.group(1))
        return Turn(text="OK")


def make_client(fake_answers: dict[str, str] | None = None, **kwargs) -> Client | FakeClient:
    """Live client unless DRK_FAKE=1, in which case the canned one."""
    if FAKE:
        return FakeClient(fake_answers)
    return Client(**kwargs)
