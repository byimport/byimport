"""Repo hygiene: no secrets or personal data in tracked files.

This repo is public and ships to customers. This suite fails the build if a
tracked file contains an API-key-shaped string, a personal freemail address,
or if a credential/config file that must stay local gets committed.
"""

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Filenames that hold real credentials or account IDs and must never be tracked.
FORBIDDEN_TRACKED_FILES = re.compile(
    r"(^|/)(\.env(\..*)?|\.notfair\.json|credentials\.json|token\.json"
    r"|service-account[^/]*\.json|[^/]*-credentials\.json)$"
)

# Well-known secret token shapes. Anchored prefixes keep false positives near zero.
SECRET_PATTERNS = [
    ("Google API key", re.compile(r"AIza[0-9A-Za-z_-]{35}")),
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9]{32,}\b")),
    ("Anthropic key", re.compile(r"\bsk-ant-[A-Za-z0-9-]{32,}\b")),
    ("GitHub token", re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{36,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("Private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
]

# Personal mailbox providers. Skill docs and examples must use placeholder or
# brand-domain addresses, never a real person's inbox.
FREEMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@(gmail|googlemail|yahoo|hotmail|outlook|live|proton"
    r"|protonmail|icloud|gmx|aol)\.[a-z]{2,}\b",
    re.IGNORECASE,
)

# Obviously-fake addresses allowed in docs and tests.
FREEMAIL_ALLOWLIST = re.compile(
    r"^(user|test|example|someone|your[._-]?email|john\.?doe|jane\.?doe)[0-9]*@",
    re.IGNORECASE,
)

TEXT_EXTENSIONS = {
    ".md", ".txt", ".py", ".js", ".sh", ".json", ".yaml", ".yml", ".html",
    ".css", ".csv", ".sql", ".toml", ".cfg", ".ini", ".ics", "",
}


def tracked_files():
    out = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    )
    return [line for line in out.stdout.splitlines() if line]


def text_file_contents():
    for rel in tracked_files():
        path = REPO_ROOT / rel
        if path.suffix.lower() not in TEXT_EXTENSIONS or not path.is_file():
            continue
        try:
            yield rel, path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue


def test_no_credential_files_tracked():
    offenders = [f for f in tracked_files() if FORBIDDEN_TRACKED_FILES.search(f)]
    assert not offenders, (
        "Credential/config files are tracked and would ship publicly: "
        f"{offenders}. Remove them with `git rm --cached` and keep them in .gitignore."
    )


def test_no_secret_tokens_in_tracked_files():
    findings = []
    for rel, content in text_file_contents():
        for label, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(content):
                line = content.count("\n", 0, match.start()) + 1
                findings.append(f"{rel}:{line} — {label}")
    assert not findings, (
        "Possible secrets committed to this public repo:\n" + "\n".join(findings)
    )


def test_no_personal_email_addresses_in_tracked_files():
    findings = []
    for rel, content in text_file_contents():
        for match in FREEMAIL_PATTERN.finditer(content):
            if FREEMAIL_ALLOWLIST.match(match.group(0)):
                continue
            line = content.count("\n", 0, match.start()) + 1
            findings.append(f"{rel}:{line} — {match.group(0)}")
    assert not findings, (
        "Personal email addresses committed to this public repo:\n"
        + "\n".join(findings)
        + "\nUse a placeholder (user@example.com) or a brand-domain address instead."
    )
