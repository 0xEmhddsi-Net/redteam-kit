"""Minimal OpenAI-compatible client with JSONL run recording.

Never imports a vendor SDK: the endpoint is a URL, the payload is JSON, and the
transcript is the evidence.
"""

from __future__ import annotations

import json
import os
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
            raise SystemExit("DEEPSEEK_API_KEY is not set (use DRK_FAKE=1 for offline)")
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
                    time.sleep(min(2**attempt * 2, 60))
                    continue
                response.raise_for_status()
                body = response.json()
                text = body["choices"][0]["message"].get("
