#!/usr/bin/env python3
"""AI content review for adaptive-learner-content (EXP-033 / AIV-06).

Advisory-only PR check: sends the cards from every lesson file CHANGED
in the PR to an LLM grader and posts the findings as a PR comment. This
catches semantic errors ``validate_content.py`` (schema) and
``audit_content.py`` (deterministic duplicate/structure checks, EXP-032)
cannot — a wrong article, a mismatched conjugation, a plausible-looking
but wrong distractor. Never blocks: the exit code is always 0.

Skipped entirely (no API call, no comment, no cost) when the ``OPENAI_KEY``
secret is absent, so a fork or a repo without the secret configured stays
green. Runs on ``pull_request`` only (see the workflow), not on every push
- that is where the cost control lives; per-run the cap is a hard
``MAX_CARDS_PER_RUN``.

The prompt and the defensive JSON-response parser are a deliberate port
of ``adaptive-learner/frontend/src/lib/ai/validation/content-validator.ts``
(AIV-01, the app-side "Mit KI pruefen" button) - same grading criteria,
same batch size, same JSON contract, so a CI-side and an app-side review
of the same cards agree.

Usage::

    python scripts/ai_review.py --base origin/main --head HEAD
    python scripts/ai_review.py --files sets/de/es-a1/lessons/01-x.json --dry-run
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

VALIDATION_BATCH_SIZE = 10
MAX_CARDS_PER_RUN = 500
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
COMMENT_MARKER = "<!-- ai-review-bot:aiv-06 -->"


class ValidationParseError(Exception):
    """A non-trivial AI response contained no recoverable JSON array."""


# --- pure: batching + prompt + parsing (ported from content-validator.ts) --


def split_into_batches(cards: list[dict], batch_size: int = VALIDATION_BATCH_SIZE) -> list[list[dict]]:
    size = max(1, batch_size)
    return [cards[i : i + size] for i in range(0, len(cards), size)]


def build_validation_prompt(
    cards: list[dict], source_language: str, target_language: str, level: str
) -> str:
    card_json = json.dumps(
        [
            {
                "card_id": c["id"],
                "front": c.get("front", ""),
                "back": c.get("back", ""),
                "notes": c.get("notes"),
            }
            for c in cards
        ],
        ensure_ascii=False,
    )
    return "\n".join(
        [
            "Du bist ein Sprachlehrer und Qualitaetspruefer.",
            f"Pruefe diese Lernkarten (Quellsprache: {source_language}, "
            f"Zielsprache: {target_language}, Level: {level}).",
            "Das Feld 'front' ist in der Zielsprache, 'back' und 'notes' in der Quellsprache.",
            "",
            "Pro Karte pruefen:",
            "1. Uebersetzung korrekt?",
            "2. Artikel korrekt?",
            "3. Konjugation korrekt?",
            "4. Akzente vollstaendig?",
            "5. Distraktoren plausibel aber eindeutig falsch?",
            "6. Cloze-Luecke hat genau eine korrekte Antwort?",
            "",
            "Antworte NUR als JSON Array, exakt in dieser Form:",
            '[{"card_id": "...", "ok": true, "issues": []},',
            ' {"card_id": "...", "ok": false, "issues": '
            '[{"field": "back", "problem": "...", "suggestion": "..."}]}]',
            "Eine Karte ohne Probleme hat ok=true und issues=[].",
            "Schreibe 'problem' und 'suggestion' in der Quellsprache.",
            "Keine Erklaerungen ausserhalb des JSON.",
            "",
            "Karten:",
            card_json,
        ]
    )


def _find_first_balanced_array(text: str) -> str | None:
    start = text.find("[")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    return None


def _strip_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return stripped


def parse_validation_response(text: str) -> list[dict]:
    """Defensive parse. An empty response or a literal ``[]`` means "all
    cards OK" and yields ``[]`` - not an error. A non-trivial response
    with no recoverable array raises {@link ValidationParseError}."""
    if not isinstance(text, str):
        raise ValidationParseError("Response was not a string")
    stripped = _strip_fences(text)
    if not stripped:
        return []

    array_text = _find_first_balanced_array(stripped)
    if array_text is None:
        raise ValidationParseError("No JSON array found in response")
    try:
        data = json.loads(array_text)
    except json.JSONDecodeError as exc:
        raise ValidationParseError(f"Response array could not be parsed: {exc}") from exc
    if not isinstance(data, list):
        raise ValidationParseError("Parsed JSON was not an array")

    results: list[dict] = []
    for row in data:
        if not isinstance(row, dict):
            continue
        card_id = row.get("card_id")
        if not isinstance(card_id, str) or not card_id:
            continue
        issues_raw = row.get("issues")
        issues = []
        if isinstance(issues_raw, list):
            for raw in issues_raw:
                if not isinstance(raw, dict):
                    continue
                field = raw.get("field", "")
                problem = raw.get("problem", "")
                suggestion = raw.get("suggestion", "")
                if not (field or problem or suggestion):
                    continue
                issues.append({"field": field, "problem": problem, "suggestion": suggestion})
        ok = row.get("ok") if isinstance(row.get("ok"), bool) else len(issues) == 0
        if issues:
            ok = False
        results.append({"card_id": card_id, "ok": ok, "issues": issues})
    return results


# --- IO: git diff, manifest lookup, provider call, PR comment --------------


def changed_lesson_files(base_ref: str, head_ref: str) -> list[Path]:
    """Lesson JSON files changed between ``base_ref`` and ``head_ref``
    that still exist (deleted files have nothing to review)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=d", f"{base_ref}...{head_ref}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    files = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or "/lessons/" not in line or not line.endswith(".json"):
            continue
        path = REPO_ROOT / line
        if path.is_file():
            files.append(path)
    return files


def set_context_for(lesson_path: Path) -> dict | None:
    """Resolve the language pair + level for a lesson file from its
    set's own ``manifest.yaml`` (sibling of the ``lessons/`` dir)."""
    set_dir = lesson_path.parent.parent
    manifest_path = set_dir / "manifest.yaml"
    if not manifest_path.is_file():
        return None
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    sets = manifest.get("sets") or []
    if not sets:
        return None
    entry = sets[0]
    return {
        "source_language": entry.get("source_language", "?"),
        "target_language": entry.get("target_language", "?"),
        "level": entry.get("level", "?"),
    }


def call_openai(prompt: str, api_key: str, model: str = OPENAI_MODEL) -> tuple[str, str]:
    """Returns (response_text, response_id)."""
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    text = data["choices"][0]["message"]["content"]
    response_id = data.get("id", "")
    return text, response_id


def render_markdown_report(
    findings_by_file: dict[str, list[dict]],
    parse_errors: list[str],
    reviewed_cards: int,
    truncated: bool,
) -> str:
    lines = [COMMENT_MARKER, "## AI content review (AIV-06, advisory)", ""]
    total_issues = sum(
        1 for results in findings_by_file.values() for r in results if not r["ok"]
    )
    if reviewed_cards == 0:
        lines.append("No changed lesson cards in this PR to review.")
        return "\n".join(lines)

    lines.append(f"Reviewed {reviewed_cards} card(s) across {len(findings_by_file)} file(s).")
    if truncated:
        lines.append(
            f"⚠️ Cut off at {MAX_CARDS_PER_RUN} cards (cost cap) - not every changed "
            "card in this PR was reviewed."
        )
    lines.append("")

    if total_issues == 0 and not parse_errors:
        lines.append("✅ No issues found.")
    for file_label, results in findings_by_file.items():
        flagged = [r for r in results if not r["ok"]]
        if not flagged:
            continue
        lines.append(f"### `{file_label}`")
        for r in flagged:
            lines.append(f"- **{r['card_id']}**")
            for issue in r["issues"]:
                field = issue["field"] or "?"
                problem = issue["problem"] or "(no description)"
                suggestion = issue["suggestion"]
                suffix = f" → {suggestion}" if suggestion else ""
                lines.append(f"  - `{field}`: {problem}{suffix}")
        lines.append("")

    if parse_errors:
        lines.append("### Could not parse")
        for err in parse_errors:
            lines.append(f"- {err}")

    lines.append("")
    lines.append(f"_Model: {OPENAI_MODEL} - this check is advisory, never blocking._")
    return "\n".join(lines)


def find_existing_comment(repo: str, pr_number: int, token: str) -> int | None:
    resp = requests.get(
        f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
        params={"per_page": 100},
        timeout=30,
    )
    resp.raise_for_status()
    for comment in resp.json():
        if COMMENT_MARKER in (comment.get("body") or ""):
            return comment["id"]
    return None


def post_or_update_pr_comment(repo: str, pr_number: int, token: str, body: str) -> None:
    existing_id = find_existing_comment(repo, pr_number, token)
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    if existing_id is not None:
        requests.patch(
            f"https://api.github.com/repos/{repo}/issues/comments/{existing_id}",
            headers=headers,
            json={"body": body},
            timeout=30,
        ).raise_for_status()
    else:
        requests.post(
            f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments",
            headers=headers,
            json={"body": body},
            timeout=30,
        ).raise_for_status()


def pr_number_from_event() -> int | None:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path or not Path(event_path).is_file():
        return None
    event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    pr = event.get("pull_request") or {}
    return pr.get("number")


# --- orchestration -----------------------------------------------------


def review_files(files: list[Path], api_key: str) -> tuple[dict[str, list[dict]], list[str], int, bool]:
    findings_by_file: dict[str, list[dict]] = {}
    parse_errors: list[str] = []
    reviewed = 0
    truncated = False

    for path in files:
        if reviewed >= MAX_CARDS_PER_RUN:
            truncated = True
            break
        context = set_context_for(path)
        if context is None:
            continue
        lesson = json.loads(path.read_text(encoding="utf-8"))
        cards = lesson.get("cards", []) or []
        remaining = MAX_CARDS_PER_RUN - reviewed
        if len(cards) > remaining:
            cards = cards[:remaining]
            truncated = True
        try:
            label = str(path.relative_to(REPO_ROOT))
        except ValueError:
            label = str(path)
        file_results: list[dict] = []
        for batch in split_into_batches(cards):
            prompt = build_validation_prompt(
                batch,
                context["source_language"],
                context["target_language"],
                context["level"],
            )
            try:
                text, _response_id = call_openai(prompt, api_key)
                file_results.extend(parse_validation_response(text))
            except ValidationParseError as exc:
                parse_errors.append(f"{label}: {exc}")
            reviewed += len(batch)
        findings_by_file[label] = file_results

    return findings_by_file, parse_errors, reviewed, truncated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=None, help="git ref for the PR base")
    parser.add_argument("--head", default="HEAD", help="git ref for the PR head")
    parser.add_argument("--files", nargs="*", default=None, help="explicit lesson files (skips git diff)")
    parser.add_argument("--dry-run", action="store_true", help="print the report, never post a comment")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_KEY")
    if not api_key:
        print("OPENAI_KEY not set - skipping AI review (advisory check, nothing to do).")
        return 0

    if args.files:
        files = [Path(f) for f in args.files]
    elif args.base:
        files = changed_lesson_files(args.base, args.head)
    else:
        print("Need --files or --base to know what changed - skipping.", file=sys.stderr)
        return 0

    if not files:
        print("No changed lesson files - skipping AI review.")
        return 0

    findings_by_file, parse_errors, reviewed, truncated = review_files(files, api_key)
    report = render_markdown_report(findings_by_file, parse_errors, reviewed, truncated)
    print(report)

    if args.dry_run:
        return 0

    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    pr_number = pr_number_from_event()
    if not (token and repo and pr_number):
        print("Not running in a PR context (no token/repo/PR number) - report printed above only.")
        return 0

    post_or_update_pr_comment(repo, pr_number, token, report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
