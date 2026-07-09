#!/usr/bin/env python3
"""Validate the EXTERNAL repos listed in ``recommended-repos.json``.

For every non-``self`` entry this clones the repo, checks out the
pinned ``commit``, and verifies the snapshot is fit to join the
federated search:

  1. the ``commit`` exists and is reachable from the declared ``branch``
     (you cannot pin a commit that the branch does not contain);
  2. the snapshot ships a ``search-index.json`` that matches
     ``schema/search-index.schema.json`` (the federation contract);
  3. that index's ``repo`` slug matches the entry's URL.

This is the online counterpart to ``validate_registry.py`` (which does
the offline, file-shape checks). Run it in the PR gate so a repo can
only be admitted once its pinned commit actually validates.

The ``self`` entry is skipped: it is branch-tracked and validated by
this repo's own CI, not fetched over the network.

Usage:
  python scripts/validate_registered_repo.py
  python scripts/validate_registered_repo.py <url>   # one repo only

Exit code 0 if every checked repo passes, 1 otherwise.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import jsonschema

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "recommended-repos.json"
INDEX_SCHEMA = REPO_ROOT / "schema" / "search-index.schema.json"


def _slug(url: str) -> str:
    return url.rstrip("/").removeprefix("https://github.com/").lower()


def _run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def validate_repo(entry: dict, index_schema: dict) -> list[str]:
    url = entry.get("url", "")
    branch = entry.get("branch", "")
    commit = entry.get("commit", "")
    errors: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "repo"
        clone = _run(["git", "clone", "--branch", branch, url, str(work)])
        if clone.returncode != 0:
            return [f"{url}: cannot clone branch {branch!r}: {clone.stderr.strip()}"]

        # The commit must exist...
        if _run(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=work).returncode != 0:
            return [f"{url}: commit {commit} not found in the repo"]
        # ...and be reachable from the declared branch.
        ancestry = _run(
            ["git", "merge-base", "--is-ancestor", commit, f"origin/{branch}"], cwd=work
        )
        if ancestry.returncode != 0:
            errors.append(f"{url}: commit {commit} is not on branch {branch!r}")

        _run(["git", "checkout", "--quiet", commit], cwd=work)

        index_path = work / "search-index.json"
        if not index_path.is_file():
            errors.append(f"{url}: no search-index.json at commit {commit[:12]}")
            return errors

        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{url}: search-index.json is invalid JSON: {exc}")
            return errors

        validator = jsonschema.Draft202012Validator(index_schema)
        for err in sorted(validator.iter_errors(index), key=lambda e: list(e.path)):
            loc = "/".join(str(p) for p in err.path) or "(root)"
            errors.append(f"{url}: search-index.json: {loc}: {err.message}")

        index_slug = str(index.get("repo", "")).lower()
        if index_slug and index_slug != _slug(url):
            errors.append(
                f"{url}: search-index.json repo {index.get('repo')!r} "
                f"does not match the registered url"
            )

    return errors


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    only = argv[0] if argv else None

    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    index_schema = json.loads(INDEX_SCHEMA.read_text(encoding="utf-8"))

    external = [
        r
        for r in (data.get("repos") or [])
        if not r.get("self") and (only is None or _slug(r.get("url", "")) == _slug(only))
    ]

    if not external:
        print("No external repos to validate.")
        return 0

    all_errors: list[str] = []
    for entry in external:
        url = entry.get("url", "?")
        errors = validate_repo(entry, index_schema)
        if errors:
            print(f"FAIL {url}")
            for e in errors:
                print(f"  - {e}")
            all_errors.extend(errors)
        else:
            print(f"PASS {url} @ {entry.get('commit', '')[:12]}")

    if all_errors:
        print(f"\n{len(all_errors)} error(s) across registered repos.", file=sys.stderr)
        return 1
    print(f"\nAll {len(external)} registered repo(s) validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
