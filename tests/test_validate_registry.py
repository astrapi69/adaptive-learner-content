"""The registry gate (``validate_registry.py``) enforces the pinning rules.

``recommended-repos.json`` is the seed list the app federates its
cross-repo search over. The offline validator guards the file shape and
the cross-field rules the JSON Schema cannot fully express: exactly one
branch-tracked ``self`` entry, and every OTHER entry pinned to a
validated commit. These tests pin that contract.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_registry as vr  # noqa: E402


def _write(tmp_path: Path, data: dict, monkeypatch) -> None:
    path = tmp_path / "recommended-repos.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(vr, "REGISTRY_PATH", path)


def test_committed_registry_is_valid() -> None:
    """The registry that actually ships must pass its own gate."""
    assert vr.validate() == []


def test_external_entry_requires_commit_and_validation(tmp_path, monkeypatch) -> None:
    _write(
        tmp_path,
        {
            "repos": [
                {
                    "url": "https://github.com/coach/x",
                    "branch": "main",
                    "title": "X",
                    "trust_level": 1,
                }
            ]
        },
        monkeypatch,
    )
    errors = vr.validate()
    assert any("commit" in e for e in errors), errors


def test_self_entry_must_not_pin_commit(tmp_path, monkeypatch) -> None:
    _write(
        tmp_path,
        {
            "repos": [
                {
                    "url": "https://github.com/astrapi69/adaptive-learner-content",
                    "branch": "main",
                    "title": "Official Content",
                    "trust_level": 3,
                    "self": True,
                    "commit": "0" * 40,
                }
            ]
        },
        monkeypatch,
    )
    errors = vr.validate()
    assert any("branch-tracked" in e for e in errors), errors


def test_pending_entry_is_rejected(tmp_path, monkeypatch) -> None:
    _write(
        tmp_path,
        {
            "repos": [
                {
                    "url": "https://github.com/coach/x",
                    "branch": "main",
                    "title": "X",
                    "trust_level": 1,
                    "commit": "a" * 40,
                    "validation": {
                        "status": "pending",
                        "validated_at": "2026-07-09T00:00:00Z",
                    },
                }
            ]
        },
        monkeypatch,
    )
    errors = vr.validate()
    assert any("validated" in e for e in errors), errors


def test_duplicate_urls_rejected(tmp_path, monkeypatch) -> None:
    entry = {
        "url": "https://github.com/coach/x",
        "branch": "main",
        "title": "X",
        "trust_level": 1,
        "commit": "a" * 40,
        "validation": {"status": "validated", "validated_at": "2026-07-09T00:00:00Z"},
    }
    _write(tmp_path, {"repos": [entry, dict(entry)]}, monkeypatch)
    errors = vr.validate()
    assert any("duplicate" in e for e in errors), errors
