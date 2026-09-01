"""Tests for the read-only set exporter (``scripts/export_set.py``).

The exporter snapshots ONE set's lessons into a single YAML/JSON file for
AI-assisted review. It is explicitly NOT a re-import format: changes flow
only through the individual schema-validated lesson JSON files.

Covered behaviours (TDD, RED first):
* a known set exports with the correct ``lesson_count`` and the lesson
  order of the set manifest's ``metadata.lessons`` list,
* umlauts survive as REAL UTF-8 in the written bytes (never ``\\u00fc``
  escapes, never an ae/oe/ue substitution),
* re-parsing the YAML yields content equal to the source lesson JSONs,
* an unknown slug fails with a non-zero exit and lists the available sets,
* ``--format json`` produces valid JSON with the same lesson content,
* the default output path lands under ``exports/`` (created on demand),
* the manifest set id (``adaptive-learner-app-from-de``) resolves the same set as
  the path basename slug,
* equal path basenames under several source-language directories
  (``fr-a1`` under ``sets/en``, ``sets/de``, ``sets/el``) are
  disambiguated by ``--lang``; no match for the given lang errors.
* ``--split-size`` splits a large set's export into several
  self-contained files (each carrying its own ``review_instructions``
  copy plus ``part``/``of``/``lesson_count``/``total_lesson_count``),
  in consecutive, order-preserving chunks; it rejects being combined
  with ``--out``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import export_set  # noqa: E402

KNOWN_SLUG = "adaptive-learner-app"
KNOWN_SET_DIR = REPO_ROOT / "sets" / "de" / "adaptive-learner-app"


def load_source_lessons() -> list[dict]:
    """Load the known set's lesson JSONs in set-manifest order."""
    set_manifest = yaml.safe_load(
        (KNOWN_SET_DIR / "manifest.yaml").read_text(encoding="utf-8")
    )
    lesson_filenames = set_manifest["metadata"]["lessons"]
    return [
        json.loads((KNOWN_SET_DIR / "lessons" / lesson_filename).read_text(encoding="utf-8"))
        for lesson_filename in lesson_filenames
    ]


def run_export(tmp_path: Path, *extra_argv: str) -> Path:
    """Run the exporter for the known set into ``tmp_path`` and return the file."""
    suffix = "json" if "json" in extra_argv else "yaml"
    out_path = tmp_path / f"export.{suffix}"
    exit_code = export_set.main([KNOWN_SLUG, "--out", str(out_path), *extra_argv])
    assert exit_code == 0
    return out_path


def test_known_set_exports_with_count_and_manifest_order(tmp_path: Path) -> None:
    out_path = run_export(tmp_path)
    export_payload = yaml.safe_load(out_path.read_text(encoding="utf-8"))

    source_lessons = load_source_lessons()
    assert export_payload["set"] == KNOWN_SLUG
    assert export_payload["language"] == "de"
    assert export_payload["lesson_count"] == len(source_lessons)
    assert len(export_payload["lessons"]) == len(source_lessons)
    exported_ids = [lesson["id"] for lesson in export_payload["lessons"]]
    source_ids = [lesson["id"] for lesson in source_lessons]
    assert exported_ids == source_ids


def test_metadata_header_fields_in_spec_order(tmp_path: Path) -> None:
    out_path = run_export(tmp_path)
    export_payload = yaml.safe_load(out_path.read_text(encoding="utf-8"))

    pinned_version = (REPO_ROOT / "schema" / "engine-version.txt").read_text(
        encoding="utf-8"
    ).strip()
    assert export_payload["engine_version"] == pinned_version
    # ISO-8601 UTC, e.g. 2026-07-11T12:34:56Z
    assert export_payload["generated_at"].endswith("Z")
    assert "T" in export_payload["generated_at"]
    # Exact top-level field order of the export spec.
    assert list(export_payload.keys()) == [
        "review_instructions",
        "set",
        "language",
        "engine_version",
        "generated_at",
        "lesson_count",
        "lessons",
    ]


def test_umlauts_survive_as_real_utf8(tmp_path: Path) -> None:
    out_path = run_export(tmp_path)
    raw_text = out_path.read_bytes().decode("utf-8")

    assert "ü" in raw_text
    assert "ä" in raw_text
    assert "\\u00fc" not in raw_text
    assert "\\u00e4" not in raw_text
    # A known lesson word must keep its umlaut, never an ue-substitution.
    # (Lowercase "ausfuehrungsmodell" DOES occur as an ASCII lesson id, so
    # assert on the capitalized prose word, not the token.)
    assert "Übungen" in raw_text
    assert "Uebungen" not in raw_text


def test_yaml_reparse_content_equals_source_lessons(tmp_path: Path) -> None:
    out_path = run_export(tmp_path)
    export_payload = yaml.safe_load(out_path.read_text(encoding="utf-8"))
    assert export_payload["lessons"] == load_source_lessons()


def test_format_json_is_valid_and_content_equal(tmp_path: Path) -> None:
    out_path = run_export(tmp_path, "--format", "json")
    raw_text = out_path.read_text(encoding="utf-8")

    export_payload = json.loads(raw_text)
    assert export_payload["lessons"] == load_source_lessons()
    # ensure_ascii must be off: real umlauts in the JSON bytes too.
    assert "Übungen" in raw_text
    assert "\\u00fc" not in raw_text


def test_unknown_slug_fails_and_lists_available_sets(tmp_path: Path, capsys) -> None:
    exit_code = export_set.main(
        ["definitely-not-a-set", "--out", str(tmp_path / "never-written.yaml")]
    )
    assert exit_code != 0
    captured_stderr = capsys.readouterr().err
    assert "definitely-not-a-set" in captured_stderr
    assert KNOWN_SLUG in captured_stderr
    assert not (tmp_path / "never-written.yaml").exists()


def test_manifest_id_resolves_like_path_basename(tmp_path: Path) -> None:
    out_path = tmp_path / "by-id.yaml"
    exit_code = export_set.main(["adaptive-learner-app-from-de", "--out", str(out_path)])
    assert exit_code == 0
    export_payload = yaml.safe_load(out_path.read_text(encoding="utf-8"))
    assert export_payload["set"] == "adaptive-learner-app-from-de"
    assert export_payload["lessons"] == load_source_lessons()


def test_lang_disambiguates_equal_basenames(tmp_path: Path) -> None:
    # fr-a1 exists under sets/en, sets/de and sets/el; --lang picks the
    # source-language directory.
    out_path = tmp_path / "fr-a1-el.yaml"
    exit_code = export_set.main(["fr-a1", "--lang", "el", "--out", str(out_path)])
    assert exit_code == 0
    export_payload = yaml.safe_load(out_path.read_text(encoding="utf-8"))

    el_set_manifest = yaml.safe_load(
        (REPO_ROOT / "sets" / "el" / "fr-a1" / "manifest.yaml").read_text(
            encoding="utf-8"
        )
    )
    assert export_payload["language"] == "el"
    assert export_payload["lesson_count"] == len(
        el_set_manifest["metadata"]["lessons"]
    )


def test_lang_without_match_errors_listing_candidates(
    tmp_path: Path, capsys
) -> None:
    # fr-a1 does not exist under sets/hi: ambiguous basename, no lang match.
    exit_code = export_set.main(
        ["fr-a1", "--lang", "hi", "--out", str(tmp_path / "never-written.yaml")]
    )
    assert exit_code != 0
    captured_stderr = capsys.readouterr().err
    assert "fr-a1" in captured_stderr
    assert "fr-a1-from-en" in captured_stderr
    assert not (tmp_path / "never-written.yaml").exists()


def test_default_out_path_lands_under_exports_dir() -> None:
    exports_dir = REPO_ROOT / "exports"
    before_export = set(exports_dir.glob("*")) if exports_dir.is_dir() else set()
    exit_code = export_set.main([KNOWN_SLUG])
    assert exit_code == 0
    created_files = set(exports_dir.glob(f"{KNOWN_SLUG}-de-*.yaml")) - before_export
    assert len(created_files) == 1
    created_export = created_files.pop()
    try:
        export_payload = yaml.safe_load(created_export.read_text(encoding="utf-8"))
        assert export_payload["set"] == KNOWN_SLUG
    finally:
        created_export.unlink()


REVIEW_TEMPLATE_PATH = REPO_ROOT / "docs" / "ai-review-prompt-template.md"


def test_review_instructions_is_first_field_and_equals_template(tmp_path: Path) -> None:
    out_path = run_export(tmp_path)
    raw_text = out_path.read_text(encoding="utf-8")
    export_payload = yaml.safe_load(raw_text)

    template_text = REVIEW_TEMPLATE_PATH.read_text(encoding="utf-8")
    assert export_payload["review_instructions"] == template_text
    assert list(export_payload.keys())[0] == "review_instructions"
    # First field of the raw output too, before all metadata and lessons,
    # rendered as a readable YAML block scalar.
    assert raw_text.startswith("review_instructions: |")


def test_review_instructions_block_scalar_roundtrips_exactly(tmp_path: Path) -> None:
    out_path = run_export(tmp_path)
    export_payload = yaml.safe_load(out_path.read_text(encoding="utf-8"))
    # The block-scalar rendering must not bend the text: re-parsing yields
    # EXACTLY the template string, byte for byte.
    assert export_payload["review_instructions"] == REVIEW_TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )


def test_review_instructions_umlauts_stay_real_utf8_in_json(tmp_path: Path) -> None:
    out_path = run_export(tmp_path, "--format", "json")
    raw_text = out_path.read_text(encoding="utf-8")

    export_payload = json.loads(raw_text)
    assert list(export_payload.keys())[0] == "review_instructions"
    assert export_payload["review_instructions"] == REVIEW_TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )
    # A known template phrase keeps its umlauts in the written JSON bytes.
    assert "Prüfkategorien" in raw_text
    assert "\\u00fc" not in raw_text


def test_missing_review_template_fails_with_clear_error(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    monkeypatch.setattr(
        export_set, "REVIEW_TEMPLATE_PATH", tmp_path / "not-there.md"
    )
    out_path = tmp_path / "never-written.yaml"
    exit_code = export_set.main([KNOWN_SLUG, "--out", str(out_path)])
    assert exit_code != 0
    captured_stderr = capsys.readouterr().err
    assert "ai-review-prompt-template" in captured_stderr or "not-there.md" in captured_stderr
    assert not out_path.exists()


def test_chunk_lessons_splits_into_consecutive_groups_preserving_order() -> None:
    lessons = [{"id": f"l{i}"} for i in range(8)]
    chunks = export_set.chunk_lessons(lessons, 5)
    assert chunks == [lessons[0:5], lessons[5:8]]


def test_chunk_lessons_split_size_at_or_above_count_yields_one_chunk() -> None:
    lessons = [{"id": f"l{i}"} for i in range(3)]
    assert export_set.chunk_lessons(lessons, 5) == [lessons]
    assert export_set.chunk_lessons(lessons, 3) == [lessons]


def test_chunk_lessons_rejects_non_positive_split_size() -> None:
    with pytest.raises(ValueError):
        export_set.chunk_lessons([{"id": "l0"}], 0)


EXPORTS_DIR = REPO_ROOT / "exports"


def run_split_export(tmp_path: Path, split_size: int, *extra_argv: str) -> list[Path]:
    """Run a split export for the known set and return the written files,
    sorted by name (which sorts by part number thanks to zero-padding)."""
    before = set(EXPORTS_DIR.glob("*")) if EXPORTS_DIR.is_dir() else set()
    exit_code = export_set.main(
        [KNOWN_SLUG, "--split-size", str(split_size), *extra_argv]
    )
    assert exit_code == 0
    created = sorted((set(EXPORTS_DIR.glob("*")) - before))
    for created_path in created:
        tmp_path_copy = tmp_path / created_path.name
        tmp_path_copy.write_bytes(created_path.read_bytes())
        created_path.unlink()
    return sorted(tmp_path.glob("*"))


def test_split_size_writes_one_file_per_chunk_with_correct_lesson_counts(
    tmp_path: Path,
) -> None:
    source_lessons = load_source_lessons()
    assert len(source_lessons) == 12  # KNOWN_SLUG fixture assumption

    created_files = run_split_export(tmp_path, 8)
    assert len(created_files) == 2

    part_1 = yaml.safe_load(created_files[0].read_text(encoding="utf-8"))
    part_2 = yaml.safe_load(created_files[1].read_text(encoding="utf-8"))
    assert part_1["lesson_count"] == 8
    assert part_2["lesson_count"] == 4
    assert part_1["total_lesson_count"] == 12
    assert part_2["total_lesson_count"] == 12
    assert part_1["part"] == 1
    assert part_1["of"] == 2
    assert part_2["part"] == 2
    assert part_2["of"] == 2


def test_split_size_parts_concatenate_to_the_full_lesson_order(tmp_path: Path) -> None:
    source_lessons = load_source_lessons()
    created_files = run_split_export(tmp_path, 5)

    reassembled: list[dict] = []
    for created_path in created_files:
        payload = yaml.safe_load(created_path.read_text(encoding="utf-8"))
        reassembled.extend(payload["lessons"])
    assert reassembled == source_lessons


def test_split_size_each_part_is_self_contained_with_review_instructions(
    tmp_path: Path,
) -> None:
    created_files = run_split_export(tmp_path, 8)
    template_text = REVIEW_TEMPLATE_PATH.read_text(encoding="utf-8")
    for created_path in created_files:
        payload = yaml.safe_load(created_path.read_text(encoding="utf-8"))
        assert payload["review_instructions"] == template_text


def test_split_size_at_or_above_lesson_count_yields_single_file(tmp_path: Path) -> None:
    created_files = run_split_export(tmp_path, 100)
    assert len(created_files) == 1
    payload = yaml.safe_load(created_files[0].read_text(encoding="utf-8"))
    assert payload["part"] == 1
    assert payload["of"] == 1
    assert payload["lesson_count"] == payload["total_lesson_count"]


def test_split_size_combined_with_out_is_a_usage_error(tmp_path: Path, capsys) -> None:
    exit_code = export_set.main(
        [
            KNOWN_SLUG,
            "--split-size",
            "5",
            "--out",
            str(tmp_path / "never-written.yaml"),
        ]
    )
    assert exit_code != 0
    captured_stderr = capsys.readouterr().err
    assert "--split-size" in captured_stderr
    assert "--out" in captured_stderr
    assert not (tmp_path / "never-written.yaml").exists()
