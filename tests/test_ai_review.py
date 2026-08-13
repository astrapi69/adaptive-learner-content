#!/usr/bin/env python3
"""Tests for the AI content review CI action (EXP-033 / AIV-06).

Everything runs offline - every ``requests`` call is mocked. The prompt
+ parser are a deliberate port of the app-side
``content-validator.ts`` (AIV-01); the parser tests mirror that
module's own test cases (prose-wrapped JSON, markdown fences, an empty
response meaning "all OK", an unparseable response raising).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import ai_review as air  # noqa: E402


# --- pure: batching -----------------------------------------------------


def test_split_into_batches_default_size():
    cards = [{"id": str(i)} for i in range(25)]
    batches = air.split_into_batches(cards)
    assert [len(b) for b in batches] == [10, 10, 5]


def test_split_into_batches_empty():
    assert air.split_into_batches([]) == []


def test_split_into_batches_exact_multiple():
    cards = [{"id": str(i)} for i in range(20)]
    assert [len(b) for b in air.split_into_batches(cards)] == [10, 10]


# --- pure: prompt ---------------------------------------------------------


def test_build_validation_prompt_contains_language_and_cards():
    cards = [{"id": "c1", "front": "el gato", "back": "the cat"}]
    prompt = air.build_validation_prompt(cards, "en", "es", "A1")
    assert "Quellsprache: en" in prompt
    assert "Zielsprache: es" in prompt
    assert "Level: A1" in prompt
    assert "el gato" in prompt
    assert "c1" in prompt
    assert "Keine Erklaerungen ausserhalb des JSON." in prompt


# --- pure: response parsing ------------------------------------------------


def test_parse_validation_response_happy_path():
    text = json.dumps([{"card_id": "c1", "ok": True, "issues": []}])
    results = air.parse_validation_response(text)
    assert results == [{"card_id": "c1", "ok": True, "issues": []}]


def test_parse_validation_response_with_issue():
    text = json.dumps(
        [
            {
                "card_id": "c1",
                "ok": False,
                "issues": [{"field": "back", "problem": "wrong article", "suggestion": "el gato"}],
            }
        ]
    )
    results = air.parse_validation_response(text)
    assert results[0]["ok"] is False
    assert results[0]["issues"][0]["field"] == "back"


def test_parse_validation_response_prose_wrapped():
    text = "Here you go:\n" + json.dumps([{"card_id": "c1", "ok": True, "issues": []}]) + "\nDone."
    results = air.parse_validation_response(text)
    assert results[0]["card_id"] == "c1"


def test_parse_validation_response_markdown_fenced():
    text = "```json\n" + json.dumps([{"card_id": "c1", "ok": True, "issues": []}]) + "\n```"
    results = air.parse_validation_response(text)
    assert results[0]["card_id"] == "c1"


def test_parse_validation_response_empty_means_all_ok():
    assert air.parse_validation_response("") == []
    assert air.parse_validation_response("[]") == []


def test_parse_validation_response_unparseable_raises():
    with pytest.raises(air.ValidationParseError):
        air.parse_validation_response("I refuse to answer in JSON.")


def test_parse_validation_response_ok_corrected_when_issues_present():
    # A model that says ok=true but still lists an issue is corrected.
    text = json.dumps(
        [{"card_id": "c1", "ok": True, "issues": [{"field": "front", "problem": "x", "suggestion": "y"}]}]
    )
    results = air.parse_validation_response(text)
    assert results[0]["ok"] is False


# --- IO: changed_lesson_files (real throwaway git repo) --------------------


def _init_repo(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    return tmp_path


def test_changed_lesson_files_filters_to_lessons_json(tmp_path, monkeypatch):
    repo = _init_repo(tmp_path)
    monkeypatch.setattr(air, "REPO_ROOT", repo)

    lessons_dir = repo / "sets" / "en" / "es-a1" / "lessons"
    lessons_dir.mkdir(parents=True)
    (lessons_dir / "01-greetings.json").write_text("{}", encoding="utf-8")
    (repo / "README.md").write_text("hello", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "base"], cwd=repo, check=True)
    subprocess.run(["git", "branch", "base"], cwd=repo, check=True)

    (lessons_dir / "02-numbers.json").write_text("{}", encoding="utf-8")
    (repo / "README.md").write_text("hello world", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "change"], cwd=repo, check=True)

    files = air.changed_lesson_files("base", "HEAD")
    assert [f.name for f in files] == ["02-numbers.json"]


def test_changed_lesson_files_excludes_deleted(tmp_path, monkeypatch):
    repo = _init_repo(tmp_path)
    monkeypatch.setattr(air, "REPO_ROOT", repo)

    lessons_dir = repo / "sets" / "en" / "es-a1" / "lessons"
    lessons_dir.mkdir(parents=True)
    (lessons_dir / "01-greetings.json").write_text("{}", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "base"], cwd=repo, check=True)
    subprocess.run(["git", "branch", "base"], cwd=repo, check=True)

    (lessons_dir / "01-greetings.json").unlink()
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "remove"], cwd=repo, check=True)

    assert air.changed_lesson_files("base", "HEAD") == []


# --- IO: set_context_for ---------------------------------------------------


def test_set_context_for_reads_manifest(tmp_path):
    set_dir = tmp_path / "sets" / "en" / "es-a1"
    (set_dir / "lessons").mkdir(parents=True)
    manifest = {
        "sets": [{"source_language": "en", "target_language": "es", "level": "A1"}],
        "metadata": {"lessons": ["01-greetings.json"]},
    }
    (set_dir / "manifest.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    lesson_path = set_dir / "lessons" / "01-greetings.json"
    lesson_path.write_text("{}", encoding="utf-8")

    context = air.set_context_for(lesson_path)
    assert context == {"source_language": "en", "target_language": "es", "level": "A1"}


def test_set_context_for_missing_manifest_returns_none(tmp_path):
    lesson_path = tmp_path / "sets" / "en" / "es-a1" / "lessons" / "01.json"
    lesson_path.parent.mkdir(parents=True)
    lesson_path.write_text("{}", encoding="utf-8")
    assert air.set_context_for(lesson_path) is None


# --- IO: call_openai (mocked) ----------------------------------------------


def test_call_openai_returns_text_and_response_id():
    fake_response = MagicMock()
    fake_response.json.return_value = {
        "id": "chatcmpl-abc123",
        "choices": [{"message": {"content": "[]"}}],
    }
    fake_response.raise_for_status.return_value = None
    with patch.object(air.requests, "post", return_value=fake_response) as mock_post:
        text, response_id = air.call_openai("some prompt", "sk-test")
    assert text == "[]"
    assert response_id == "chatcmpl-abc123"
    _, kwargs = mock_post.call_args
    assert kwargs["headers"]["Authorization"] == "Bearer sk-test"
    assert kwargs["json"]["model"] == air.OPENAI_MODEL


# --- render_markdown_report -------------------------------------------------


def test_render_markdown_report_no_issues():
    report = air.render_markdown_report({"a.json": [{"card_id": "c1", "ok": True, "issues": []}]}, [], 1, False)
    assert "No issues found" in report
    assert air.COMMENT_MARKER in report


def test_render_markdown_report_with_issue():
    findings = {
        "a.json": [
            {
                "card_id": "c1",
                "ok": False,
                "issues": [{"field": "back", "problem": "wrong", "suggestion": "fix"}],
            }
        ]
    }
    report = air.render_markdown_report(findings, [], 1, False)
    assert "c1" in report
    assert "wrong" in report
    assert "fix" in report


def test_render_markdown_report_truncated():
    report = air.render_markdown_report({}, [], air.MAX_CARDS_PER_RUN, True)
    assert "cost cap" in report


def test_render_markdown_report_nothing_reviewed():
    report = air.render_markdown_report({}, [], 0, False)
    assert "No changed lesson cards" in report


# --- IO: PR comment find/post/update (mocked) ------------------------------


def test_post_or_update_creates_new_when_none_exists():
    list_response = MagicMock()
    list_response.json.return_value = []
    list_response.raise_for_status.return_value = None
    post_response = MagicMock()
    post_response.raise_for_status.return_value = None
    with patch.object(air.requests, "get", return_value=list_response), patch.object(
        air.requests, "post", return_value=post_response
    ) as mock_post:
        air.post_or_update_pr_comment("owner/repo", 42, "tok", "body")
    assert mock_post.called


def test_post_or_update_patches_existing_comment():
    list_response = MagicMock()
    list_response.json.return_value = [{"id": 999, "body": f"{air.COMMENT_MARKER}\nold"}]
    list_response.raise_for_status.return_value = None
    patch_response = MagicMock()
    patch_response.raise_for_status.return_value = None
    with patch.object(air.requests, "get", return_value=list_response), patch.object(
        air.requests, "patch", return_value=patch_response
    ) as mock_patch:
        air.post_or_update_pr_comment("owner/repo", 42, "tok", "new body")
    assert mock_patch.called
    assert "999" in mock_patch.call_args[0][0]


# --- orchestration: review_files --------------------------------------------


def _write_lesson_set(base: Path, cards: list[dict]) -> Path:
    set_dir = base / "sets" / "en" / "es-a1"
    lessons_dir = set_dir / "lessons"
    lessons_dir.mkdir(parents=True)
    manifest = {
        "sets": [{"source_language": "en", "target_language": "es", "level": "A1"}],
        "metadata": {"lessons": ["01.json"]},
    }
    (set_dir / "manifest.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    lesson_path = lessons_dir / "01.json"
    lesson_path.write_text(json.dumps({"cards": cards}), encoding="utf-8")
    return lesson_path


def test_review_files_happy_path(tmp_path):
    lesson_path = _write_lesson_set(tmp_path, [{"id": "c1", "front": "el gato", "back": "the cat"}])
    with patch.object(air, "call_openai", return_value=(json.dumps([{"card_id": "c1", "ok": True, "issues": []}]), "resp-1")):
        findings, errors, reviewed, truncated = air.review_files([lesson_path], "sk-test")
    assert reviewed == 1
    assert truncated is False
    assert errors == []
    assert findings[str(lesson_path)][0]["card_id"] == "c1"


def test_review_files_respects_max_cards_cap(tmp_path, monkeypatch):
    monkeypatch.setattr(air, "MAX_CARDS_PER_RUN", 5)
    cards = [{"id": f"c{i}", "front": "x", "back": "y"} for i in range(10)]
    lesson_path = _write_lesson_set(tmp_path, cards)
    with patch.object(air, "call_openai", return_value=("[]", "resp-1")) as mock_call:
        findings, errors, reviewed, truncated = air.review_files([lesson_path], "sk-test")
    assert reviewed == 5
    assert truncated is True
    assert mock_call.called


def test_review_files_skips_file_without_manifest(tmp_path):
    lesson_path = tmp_path / "sets" / "en" / "es-a1" / "lessons" / "01.json"
    lesson_path.parent.mkdir(parents=True)
    lesson_path.write_text(json.dumps({"cards": [{"id": "c1", "front": "x", "back": "y"}]}), encoding="utf-8")
    findings, errors, reviewed, truncated = air.review_files([lesson_path], "sk-test")
    assert reviewed == 0
    assert findings == {}


def test_review_files_records_parse_error_without_crashing(tmp_path):
    lesson_path = _write_lesson_set(tmp_path, [{"id": "c1", "front": "x", "back": "y"}])
    with patch.object(air, "call_openai", return_value=("not json at all, sorry", "resp-1")):
        findings, errors, reviewed, truncated = air.review_files([lesson_path], "sk-test")
    assert len(errors) == 1
    assert reviewed == 1


# --- main() gate -------------------------------------------------------------


def test_main_skips_when_no_api_key(monkeypatch, capsys):
    monkeypatch.delenv("OPENAI_KEY", raising=False)
    monkeypatch.setattr(sys, "argv", ["ai_review.py", "--files", "does-not-matter.json"])
    exit_code = air.main()
    assert exit_code == 0
    assert "OPENAI_KEY not set" in capsys.readouterr().out


def test_main_dry_run_prints_without_posting(tmp_path, monkeypatch, capsys):
    lesson_path = _write_lesson_set(tmp_path, [{"id": "c1", "front": "el gato", "back": "the cat"}])
    monkeypatch.setenv("OPENAI_KEY", "sk-test")
    monkeypatch.setattr(
        sys, "argv", ["ai_review.py", "--files", str(lesson_path), "--dry-run"]
    )
    with patch.object(air, "call_openai", return_value=("[]", "resp-1")), patch.object(
        air.requests, "post"
    ) as mock_post:
        exit_code = air.main()
    assert exit_code == 0
    assert not mock_post.called
    assert "AI content review" in capsys.readouterr().out
