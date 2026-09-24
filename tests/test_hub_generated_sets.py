"""The hub's three machine-generated language sets are marked ``generated``.

These tests pin this repository's own content (a ``repo`` row in
``.github/ownership.json``), which is why they are not part of
``tests/test_search_index_review_status.py``: that file is copied into every
content repository, and none of the others carries these sets.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import generate_search_index as gsi  # noqa: E402


def test_the_three_machine_generated_language_sets_are_marked() -> None:
    """Regression guard: ja-a1 / ko-a1 / zh-a1 are machine-generated and were
    never advertised because unverified (adaptive-learner#2161). A badge
    counting advertisable sets must not count them."""
    index, _ = gsi.build_index()
    by_id = {entry["id"]: entry for entry in index["sets"]}
    for set_id in ("ja-a1-from-de", "ko-a1-from-de", "zh-a1-from-de"):
        assert by_id[set_id]["review_status"] == "generated", set_id


def test_the_advertisable_count_excludes_them() -> None:
    index, _ = gsi.build_index()
    advertisable = [e for e in index["sets"] if e["review_status"] != "generated"]
    assert len(advertisable) == len(index["sets"]) - 3
