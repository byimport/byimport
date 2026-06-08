#!/usr/bin/env python3
"""Minimal stdlib HTTP helper (GET/POST JSON) with retry/backoff.

No external dependencies (no requests) so the pipeline runs without
``pip install``. Mirrors the retry pattern used in the repo's SEO scripts:
exponential backoff on {429, 502, 503, 504}, max 3 retries by default.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Optional

DEFAULT_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.4 Safari/605.1.15"
)
RETRYABLE = {429, 502, 503, 504}


class HttpError(RuntimeError):
    """Raised when an HTTP request fails after exhausting retries."""

    def __init__(self, message: str, status: Optional[int] = None) -> None:
        super().__init__(message)
        self.status = status


def request_json(
    url: str,
    *,
    method: str = "GET",
    headers: Optional[dict[str, str]] = None,
    params: Optional[dict[str, Any]] = None,
    body: Optional[dict[str, Any]] = None,
    form: Optional[dict[str, Any]] = None,
    timeout: int = 30,
    max_retries: int = 3,
) -> Any:
    """Perform an HTTP request and parse the JSON response.

    ``body`` is sent as JSON; ``form`` is sent url-encoded (mutually exclusive).
    Returns the decoded JSON (dict/list). Raises HttpError on failure.
    """
    if params:
        sep = "&" if urllib.parse.urlparse(url).query else "?"
        url = url + sep + urllib.parse.urlencode(params, doseq=True)

    data: Optional[bytes] = None
    hdrs = {"User-Agent": DEFAULT_UA, "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        hdrs.setdefault("Content-Type", "application/json")
    elif form is not None:
        data = urllib.parse.urlencode(form).encode("utf-8")
        hdrs.setdefault("Content-Type", "application/x-www-form-urlencoded")

    last_err: Optional[Exception] = None
    for attempt in range(max_retries + 1):
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as exc:
            last_err = exc
            if exc.code in RETRYABLE and attempt < max_retries:
                time.sleep(2 ** attempt)
                continue
            detail = ""
            try:
                detail = exc.read().decode("utf-8")[:500]
            except Exception:
                pass
            raise HttpError(f"HTTP {exc.code} for {url}: {detail}", status=exc.code)
        except (urllib.error.URLError, TimeoutError) as exc:
            last_err = exc
            if attempt < max_retries:
                time.sleep(2 ** attempt)
                continue
            raise HttpError(f"Network error for {url}: {exc}")
    raise HttpError(f"Request failed for {url}: {last_err}")
