"""The ``ai_validated`` search-index flag survives the manifest move.

``ai_validation`` is a content-repo-local provenance block (which AI
reviewed the set, when, with what result). The canonical manifest format
(engine ``content-manifest.schema.json``, strict
``additionalProperties: false``) does not know it, so it must live in the
set manifest's free-form top-level ``metadata`` block — NOT in the strict
set entry. This test pins the one consumer (``generate_search_index``):
the ki-einsteiger set keeps ``ai_validated: true`` in the index regardless
of where the block lives.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import generate_search_index as gsi  # noqa: E402


def test_ki_einsteiger_stays_ai_validated() -> None:
    index, errors = gsi.build_index(generated="2026-01-01T00:00:00Z")
    assert not errors, errors
    by_id = {s["id"]: s for s in index["sets"]}
    assert "ki-einsteiger-from-de" in by_id
    assert by_id["ki-einsteiger-from-de"]["ai_validated"] is True


def test_ai_validation_not_in_strict_set_entries() -> None:
    """No set manifest may carry ``ai_validation`` inside a set ENTRY —
    the canonical (engine) manifest schema rejects unknown fields there."""
    import yaml

    offenders = []
    for manifest_path in sorted(REPO_ROOT.glob("sets/*/*/manifest.yaml")):
        doc = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        for entry in doc.get("sets") or []:
            if "ai_validation" in entry:
                offenders.append(str(manifest_path.relative_to(REPO_ROOT)))
    assert not offenders, (
        f"ai_validation must live under the manifest's free-form metadata "
        f"block, not the strict set entry: {offenders}"
    )
