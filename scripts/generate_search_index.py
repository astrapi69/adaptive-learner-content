#!/usr/bin/env python3
"""Generate ``search-index.json`` from the content manifests.

A machine-readable catalogue of every lesson set in the repo, written
to the repo root as ``search-index.json``. It is the discovery feed an
app (or a federated index across repos) reads to list, filter and rank
sets without cloning the whole tree or parsing every lesson.

The index is ALWAYS generated — never hand-edited. The root
``manifest.yaml`` is the authoritative set list (it carries each set's
``path``); for every set we open its own ``<path>/manifest.yaml`` for
the lesson file list and book metadata, then open each lesson JSON to
count cards exactly.

Per set the index records:
  * id, name (set title), description
  * source_language, target_language (ISO 639-1 base codes), level
  * domain (default "language")
  * lesson_count: lessons actually listed in the set manifest
  * card_count: exact sum of ``cards[]`` over every lesson
  * tags: from the manifest, else []
  * ai_validated: true when the set manifest carries an ``ai_validation``
    block under its free-form ``metadata`` (set-entry fallback for older
    manifests — the canonical manifest schema keeps set entries strict)
  * trust_level: this repo's level from recommended-repos.json, else 1
  * book: the set's ``book`` block, else null
  * updated_at: ``git log -1 --format=%cI`` for the set directory

Usage:
  python scripts/generate_search_index.py
  python scripts/generate_search_index.py --check
      Regenerate in memory and compare to the committed file
      (ignoring the volatile ``generated`` timestamp). Exit 1 if the
      committed index is stale.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT_MANIFEST = REPO_ROOT / "manifest.yaml"
INDEX_PATH = REPO_ROOT / "search-index.json"
RECOMMENDED_REPOS = REPO_ROOT / "recommended-repos.json"

REPO_SLUG = "astrapi69/adaptive-learner-content"
SCHEMA_VERSION = "1.0"
DEFAULT_TRUST_LEVEL = 1

# Required, non-empty fields on every set entry in the index.
REQUIRED_SET_FIELDS = (
    "id",
    "name",
    "source_language",
    "target_language",
    "level",
    "domain",
)


def base_lang(code: str) -> str:
    return (code or "").split("-")[0].lower()


def collapse_ws(text: str | None) -> str:
    return " ".join((text or "").split())


def repo_trust_level() -> int:
    """This repo's trust level from recommended-repos.json (else default)."""
    if not RECOMMENDED_REPOS.is_file():
        return DEFAULT_TRUST_LEVEL
    try:
        data = json.loads(RECOMMENDED_REPOS.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return DEFAULT_TRUST_LEVEL
    for repo in data.get("repos") or []:
        url = (repo.get("url") or "").rstrip("/")
        if url.endswith(REPO_SLUG):
            level = repo.get("trust_level")
            if isinstance(level, int):
                return level
    return DEFAULT_TRUST_LEVEL


def git_updated_at(set_dir: Path) -> str | None:
    """Last commit date (ISO-8601) that touched ``set_dir``, or None."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(set_dir)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    stamp = out.stdout.strip()
    return stamp or None


def count_cards(set_dir: Path, lessons: list[str], errors: list[str], sid: str) -> int:
    total = 0
    for filename in lessons:
        lesson_path = set_dir / "lessons" / filename
        if not lesson_path.is_file():
            errors.append(f"set {sid}: lesson file '{filename}' is missing")
            continue
        try:
            lesson = json.loads(lesson_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"set {sid}: {filename} is invalid JSON: {exc}")
            continue
        cards = lesson.get("cards")
        if not isinstance(cards, list):
            errors.append(f"set {sid}: {filename} has no cards[] array")
            continue
        total += len(cards)
    return total


def build_set_entry(
    content_set: dict, trust_level: int, generated: str, errors: list[str]
) -> dict:
    sid = content_set.get("id", "?")
    path = content_set.get("path")
    set_dir = REPO_ROOT / path if path else None

    set_manifest: dict = {}
    set_entry: dict = content_set
    if set_dir is not None:
        manifest_path = set_dir / "manifest.yaml"
        if manifest_path.is_file():
            set_manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
            # Prefer the set's own manifest entry for metadata; fall back
            # to the root-manifest entry when the set manifest omits it.
            for s in set_manifest.get("sets") or []:
                if s.get("id") == sid:
                    set_entry = {**content_set, **{k: v for k, v in s.items() if v is not None}}
                    break
        else:
            errors.append(f"set {sid}: missing {path}/manifest.yaml")

    lessons = (set_manifest.get("metadata") or {}).get("lessons") or []
    if set_dir is not None and not lessons:
        errors.append(f"set {sid}: set manifest lists no lessons")

    card_count = count_cards(set_dir, lessons, errors, sid) if set_dir is not None else 0

    updated_at = (git_updated_at(set_dir) if set_dir is not None else None) or generated

    return {
        "id": sid,
        "name": set_entry.get("title") or set_entry.get("name") or sid,
        "description": collapse_ws(set_entry.get("description")),
        "source_language": base_lang(set_entry.get("source_language", "")),
        "target_language": base_lang(set_entry.get("target_language", "")),
        "level": (set_entry.get("level") or "").strip().lower(),
        "domain": (set_entry.get("domain") or "language").strip().lower(),
        "lesson_count": len(lessons),
        "card_count": card_count,
        "tags": list(set_entry.get("tags") or []),
        # ai_validation is repo-local provenance; the canonical (engine)
        # manifest schema keeps set entries strict, so the block lives in
        # the set manifest's free-form metadata (set-entry read kept as a
        # fallback for older manifests).
        "ai_validated": bool(
            (set_manifest.get("metadata") or {}).get("ai_validation")
            or set_entry.get("ai_validation")
        ),
        "trust_level": trust_level,
        "book": set_entry.get("book"),
        "updated_at": updated_at,
    }


def build_index(generated: str | None = None) -> tuple[dict, list[str]]:
    """Build the index dict from the manifests. Returns (index, errors)."""
    errors: list[str] = []
    if generated is None:
        generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if not ROOT_MANIFEST.is_file():
        errors.append("no root manifest.yaml")
        return {}, errors

    manifest = yaml.safe_load(ROOT_MANIFEST.read_text(encoding="utf-8")) or {}
    root_sets = manifest.get("sets") or []
    if not root_sets:
        errors.append("root manifest lists no sets")

    trust_level = repo_trust_level()

    sets = [build_set_entry(s, trust_level, generated, errors) for s in root_sets]

    index = {
        "repo": REPO_SLUG,
        "generated": generated,
        "schema_version": SCHEMA_VERSION,
        "sets": sets,
        "total_lessons": sum(s["lesson_count"] for s in sets),
        "total_cards": sum(s["card_count"] for s in sets),
    }
    validate_index(index, root_sets, errors)
    return index, errors


def validate_index(index: dict, root_sets: list[dict], errors: list[str]) -> None:
    """Schema-level checks: all sets present, no empty required fields."""
    root_ids = [s.get("id") for s in root_sets]
    index_ids = [s["id"] for s in index.get("sets", [])]
    missing = set(root_ids) - set(index_ids)
    if missing:
        errors.append(f"index missing sets: {sorted(missing)}")
    for entry in index.get("sets", []):
        for field in REQUIRED_SET_FIELDS:
            if not entry.get(field):
                errors.append(f"set {entry.get('id', '?')}: empty required field '{field}'")


def serialize(index: dict) -> str:
    return json.dumps(index, ensure_ascii=False, indent=2) + "\n"


def _comparable(index: dict) -> dict:
    """Index without the volatile ``generated`` timestamp, for --check."""
    return {k: v for k, v in index.items() if k != "generated"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed index is up to date; exit 1 if stale",
    )
    args = parser.parse_args(argv)

    index, errors = build_index()
    if errors:
        print("FAIL: search index generation errors:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    if args.check:
        if not INDEX_PATH.is_file():
            print("FAIL: search-index.json is missing (run the generator).", file=sys.stderr)
            return 1
        try:
            current = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"FAIL: search-index.json is invalid JSON: {exc}", file=sys.stderr)
            return 1
        if _comparable(current) != _comparable(index):
            print(
                "FAIL: search-index.json is stale. Run "
                "`python scripts/generate_search_index.py` and commit.",
                file=sys.stderr,
            )
            return 1
        print("search-index.json is up to date.")
        return 0

    INDEX_PATH.write_text(serialize(index), encoding="utf-8")
    print(
        f"Wrote {INDEX_PATH.name}: {len(index['sets'])} set(s), "
        f"{index['total_lessons']} lessons, {index['total_cards']} cards."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
