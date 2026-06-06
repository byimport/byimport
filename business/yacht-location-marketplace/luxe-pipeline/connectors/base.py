#!/usr/bin/env python3
"""Connector interface shared by every data source (jets and yachts).

Every source — Avinode (jets), and later MYBA/Ankor (yachts) or a scraping
fallback — implements the same contract: ``fetch()`` returns a list of dicts
conforming to schema/listing.schema.json. The rest of the pipeline
(normalisation downstream, dedup, storage, pSEO) is source-agnostic.
"""
from __future__ import annotations

import abc
import hashlib
import json
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def content_hash(payload: dict[str, Any]) -> str:
    """Stable sha256 of a payload, ignoring volatile source timestamps."""
    clone = dict(payload)
    src = dict(clone.get("source") or {})
    src.pop("scraped_at", None)
    clone["source"] = src
    clone.pop("last_seen", None)
    clone.pop("first_seen", None)
    blob = json.dumps(clone, sort_keys=True, ensure_ascii=False)
    return "sha256:" + hashlib.sha256(blob.encode("utf-8")).hexdigest()


class BaseConnector(abc.ABC):
    """Abstract data-source connector returning canonical listing dicts."""

    site: str = "base"
    asset_type: str = "jet"
    access_layer: str = "api"

    @abc.abstractmethod
    def fetch(self) -> list[dict[str, Any]]:
        """Return a list of canonical listing dicts (schema v1)."""
        raise NotImplementedError

    def make_source(self, url: str | None = None) -> dict[str, Any]:
        return {
            "site": self.site,
            "url": url,
            "scraped_at": utc_now_iso(),
            "access_layer": self.access_layer,
        }
