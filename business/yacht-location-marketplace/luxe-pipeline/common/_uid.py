#!/usr/bin/env python3
"""Path-safe per-user identifiers and secure atomic JSON writes.

Copied from seo/seo-analysis/scripts/_uid.py to keep this standalone business
tooling free of cross-directory imports. Same behaviour:

- portable_uid(): a stable, filename-safe identifier for the current user,
  used to avoid collisions in shared temp directories.
- secure_write_json(path, data): atomic, mode-0600, symlink-safe JSON write.
"""
from __future__ import annotations

import getpass
import hashlib
import json
import os
import tempfile


def portable_uid() -> str:
    """Return a short, path-safe identifier for the current user."""
    try:
        return str(os.getuid())  # POSIX
    except AttributeError:
        pass
    try:
        name = getpass.getuser()
        safe = "".join(c for c in name if c.isalnum()) or "user"
        return safe[:32]
    except Exception:
        return hashlib.sha1(os.path.expanduser("~").encode()).hexdigest()[:12]


def secure_write_json(path: str, data: object) -> str:
    """Write ``data`` as JSON to ``path`` atomically with mode 0600.

    Writes to a fresh temp file in the same directory then os.replace()s it into
    place, which is atomic and avoids symlink races on shared tmpdirs.
    """
    directory = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return path
