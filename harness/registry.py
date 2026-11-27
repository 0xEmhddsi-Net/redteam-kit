"""Package-existence checks. `None` means unknown, never "absent"."""

from __future__ import annotations

import httpx

ENDPOINTS = {
    "pypi": "https://pypi.org/pypi/{}/json",
    "npm": "https://registry.npmjs.org/{}",
}
SUSPECT = {429, 500, 502, 503, 504}


def exists(ecosystem: str, name: str, timeout: float = 15.0) -> bool | None:
    url = ENDPOINTS[ecosystem].format(name)
    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as http:
            code = http.get(url).status_code
    except httpx.HTTPError:
        return None
    if code == 200:
        return True
    if code == 404:
        return False
    return None


def normalise(name: str) -> str:
    """Keep it conservative: plausible import names only."""
    return name.strip().strip("`,.;:").lower()
