#!/usr/bin/env python3
"""Validate ``recommended-repos.json`` — the federated-search registry.

This is the fast, offline gate: it checks the registry FILE against
``schema/recommended-repos.schema.json`` and applies the cross-field
rules the JSON Schema cannot express on its own. It does NOT touch the
network — cloning and validating each external repo at its pinned
commit is the job of ``validate_registered_repo.py``.

Rules enforced here:
  * The file matches the registry JSON Schema (so every external entry
    carries a 40-char ``commit`` and a ``validation`` block; the single
    ``self`` entry is exempt).
  * At most one entry is marked ``self``, and if present its ``url``
    is this repo and it is NOT pinned to a commit (self is
    branch-tracked, validated by this repo's own CI).
  * No two entries share the same ``url``.
  * Every entry's committed ``validation.status`` is ``validated``
    (``pending`` / ``rejected`` entries must not ship in the registry).

Usage:
  python scripts/validate_registry.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "recommended-repos.json"
REGISTRY_SCHEMA = REPO_ROOT / "schema" / "recommended-repos.schema.json"

REPO_SLUG = "astrapi69/adaptive-learner-content"


def _slug(url: str) -> str:
    return url.rstrip("/").removeprefix("https://github.com/").lower()


def validate() -> list[str]:
    errors: list[str] = []

    if not REGISTRY_PATH.is_file():
        return [f"missing {REGISTRY_PATH.name}"]
    if not REGISTRY_SCHEMA.is_file():
        return [f"missing schema {REGISTRY_SCHEMA.relative_to(REPO_ROOT)}"]

    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{REGISTRY_PATH.name} is invalid JSON: {exc}"]

    schema = json.loads(REGISTRY_SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(data), key=lambda e: e.path):
        loc = "/".join(str(p) for p in err.path) or "(root)"
        errors.append(f"schema: {loc}: {err.message}")
    if errors:
        # Cross-field checks below assume a well-shaped file.
        return errors

    repos = data.get("repos") or []

    self_entries = [r for r in repos if r.get("self") is True]
    if len(self_entries) > 1:
        errors.append(f"more than one 'self' entry ({len(self_entries)})")
    for r in self_entries:
        if _slug(r.get("url", "")) != REPO_SLUG.lower():
            errors.append(f"'self' entry url must be {REPO_SLUG}, got {r.get('url')!r}")
        if r.get("commit"):
            errors.append("'self' entry must not pin a commit (it is branch-tracked)")

    seen: dict[str, int] = {}
    for i, r in enumerate(repos):
        slug = _slug(r.get("url", ""))
        if slug in seen:
            errors.append(f"duplicate repo url {r.get('url')!r} (entries {seen[slug]} and {i})")
        seen[slug] = i

        validation = r.get("validation")
        if validation is not None:
            status = validation.get("status")
            if status != "validated":
                errors.append(
                    f"{r.get('url')!r}: validation.status is {status!r}, "
                    "only 'validated' entries may ship in the registry"
                )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("FAIL: recommended-repos.json is invalid:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("recommended-repos.json is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
