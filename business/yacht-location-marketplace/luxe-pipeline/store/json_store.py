#!/usr/bin/env python3
"""Default store: write canonical listings to a JSON file (zero dependencies)."""
from __future__ import annotations

import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from common._uid import secure_write_json  # noqa: E402


def save(listings: list[dict], path: str) -> str:
    """Atomically write the listing list to ``path`` and return it."""
    return secure_write_json(path, listings)
