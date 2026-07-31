"""Set-entry ``review_status`` in the search index (engine#94).

Three states derived from ORIGIN, because origin is what makes a set
review-worthy: ``authored`` (hand-written by a speaker or domain expert,
no review needed - also the meaning of an absent field), ``generated``
(machine-generated, review pending) and ``reviewed``. Consumers derive
"advertisable as reviewed" as ``review_status != "generated"``.

The field has to reach the INDEX, not just the manifest: the index is what
a consumer reads, so a badge counting "verified sets" would otherwise count
every set as advertisable - including the machine-generated ones that must
not be advertised (adaptive-learner#2161 states they were never advertised
because unverified).
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import generate_search_index as gsi  # noqa: E402


def test_absent_review_status_means_authored() -> None:
    assert gsi.normalize_review_status(None) == "authored"


def test_each_state_passes_through() -> None:
    for state in ("authored", "generated", "reviewed"):
        assert gsi.normalize_review_status(state) == state


def test_out_of_enum_normalizes_to_authored() -> None:
    assert gsi.normalize_review_status("verified") == "authored"


def test_every_index_entry_carries_review_status() -> None:
    index, errors = gsi.build_index()
    assert not errors
    assert index["sets"]
    for entry in index["sets"]:
        assert entry["review_status"] in ("authored", "generated", "reviewed")


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
