# Import Report — orphan set `sets/de/de-b1/`

**Prepared for:** a Claude Code (cc) session to perform the import.
**Status:** unreferenced on `main` — present on disk, absent from every manifest, ignored by the loader and validator.
**Date prepared:** 2026-06-05

---

## 1. What this is

A single community-contributed lesson sitting in a set folder that was never
wired up. It predates the recent English-source PRs (#26–#29) — it comes from
commit `cb15b8e` ("Add lesson on German object pronouns and learning methods",
2026-06-03, Asterios Raptis).

```
sets/de/de-b1/
└── lessons/
    └── 01-deutsche-grammatik-objektpronomen-stellung-und-adaptive-lernmethoden.json
```

There is **no set `manifest.yaml`** in the folder, and **no entry** in the root
`manifest.yaml`, the README table, or the README directory tree.

## 2. Lesson metadata (as it exists today)

| Field | Value |
|-------|-------|
| `id` | `analysis-ed08d0f5-12f3-46ac-a524-381f42aab115` (UUID — does **not** match the filename slug) |
| `title` | Deutsche Grammatik – Objektpronomen-Stellung und adaptive Lernmethoden |
| `target_language` | `de` |
| `source_language` | `de` |
| `domain` | **`knowledge`** (a brand-new domain — not used by any other set; existing domains are `language`, `psychology`, `programming`) |
| `estimated_minutes` | 32 |
| cards | 8 (`vocab-0` … `vocab-7`; only `front`/`back`/`notes`/`tags`, no `media_type`/`difficulty`) |
| theory steps | 14 |
| exercises | 12 → matching ×2, free_text ×4, cloze ×3, word_tiles ×3 |
| extra fields | `contributed_by: "Asterios"`, `contributed_at: "2026-06-03T12:53:22.385Z"` |

Content note: the lesson mixes a genuine German-grammar topic (the
accusative-before-dative pronoun order, *Er gibt es ihr*) with meta-content
about "comparing adaptive learning methods." That second strand reads like an
app-generated analysis artifact rather than course material — worth a human
glance before publishing.

## 3. Blocking issues (MUST fix before it will validate)

`scripts/validate_content.py` enforces, per lesson:
`>=5 exercises`, `>=2 types`, `free_text: >=2 accepts AND distractors present`,
`picture_choice: distractors`.

1. **`free_text` exercises have NO distractors** — all 4 free_text items have
   `distractors: []`/missing. The validator rule (line ~171) is
   `if not ex.get("distractors"): error "...needs distractors"`. → **4 hard
   errors.** Each free_text needs **≥2 plausible wrong answers** added.
   (Accepts are fine: 2 each. Matching pairs 4 each ✓, cloze each have one
   `___` + 1 blank ✓, word_tiles 4 tiles ✓.)

2. **`id` is a UUID, not the kebab slug.** Convention across the repo is
   `id` == filename without `.json`. Change to
   `de-b1-01-objektpronomen-stellung-und-adaptive-lernmethoden` (or similar).
   Not validator-enforced, but every other lesson follows it.

3. **No set `manifest.yaml`** — must be created (see §5).

4. **Not registered** in root `manifest.yaml`, README table, or README tree.

Non-blocking but worth deciding:
- `domain: knowledge` is accepted by the validator (any non-`language` domain
  relaxes the language-pair + directory-name rules, exactly like `psychology`),
  but it introduces a **new domain vocabulary**. Decide whether to keep
  `knowledge` or reclassify (see §4).
- exercises carry no `direction` field. Non-language sets have no productive-%
  requirement, so this is fine.
- `contributed_by` / `contributed_at` are harmless to keep.

## 4. Decisions the importer needs from a human

1. **Import or discard?** It's one thin, partly meta lesson. If the goal is a
   real "German B1" course, this single file is not it. If the goal is just to
   stop it being an untracked orphan, either wire it as a 1-lesson set or delete
   the folder.
2. **Domain:** keep `domain: knowledge` (new domain) or treat as `language`
   (German-for-German B1)? Note: if `language`, the validator REQUIRES
   `source != target`, and here both are `de` → it would **fail**. So as a
   `language` set it cannot pass; it must stay a non-language domain
   (`knowledge`, or fold into an existing one).
3. **Set id / title / level / dir name.** The folder `de-b1` implies a German
   B1 *language* set, which conflicts with point 2. Suggested clean values in §5.

## 5. Proposed import procedure (once "import" + "keep domain: knowledge" are confirmed)

**Step A — fix the lesson file**
`sets/de/de-b1/lessons/01-deutsche-grammatik-objektpronomen-stellung-und-adaptive-lernmethoden.json`
- Set `id` to `de-b1-01-objektpronomen-stellung-und-adaptive-lernmethoden`.
- Add `distractors` (≥2 each) to all 4 `free_text` exercises — plausible wrong
  German answers (e.g. dative-before-accusative order *Er gibt ihr es* as a
  distractor for the *Er gibt es ihr* item).
- (Optional) drop the "adaptive Lernmethoden" meta strand if publishing as a
  grammar lesson, or split it out.
- Re-run: `python3 -c "import json; json.load(open(PATH)); print('JSON OK')"`.

**Step B — create `sets/de/de-b1/manifest.yaml`** (schema v1.3), e.g.:

```yaml
# Deutsch B1 — Wissensbausteine (Community-Beitrag) — Set-Manifest
schema_version: '1.3'
name: Deutsch B1 — Grammatik & Lernmethoden
description: >-
  Community-Lektion auf Deutsch (domain: knowledge): die
  Akkusativ-vor-Dativ-Regel bei Objektpronomen, verknüpft mit einem
  Vergleich adaptiver Lernmethoden.
sets:
  - id: de-b1-knowledge-from-de
    title: Deutsch B1 — Grammatik & Lernmethoden
    title_native: Deutsch B1
    target_language: de
    source_language: de
    domain: knowledge
    domain_label: Wissen          # mirror psych-intro's domain_label style
    level: B1
    path: sets/de/de-b1
    version: '1.0.0'
    lesson_count: 1
    description: >-
      Eine community-beigesteuerte Lektion zur Objektpronomen-Stellung
      (Akkusativ vor Dativ) mit einem Framework zum Vergleich von
      Lernmethoden. Erklärungen auf Deutsch.
    tags:
      - intermediate
      - grammar
      - german
metadata:
  author: Asterios Raptis
  license: CC-BY-SA-4.0
  lessons:
    - 01-deutsche-grammatik-objektpronomen-stellung-und-adaptive-lernmethoden.json
```

**Step C — register in root `manifest.yaml`**
Add a `de-b1-knowledge-from-de` set block (mirror the one above: id, title,
title_native, target_language de, source_language de, domain knowledge, level
B1, path sets/de/de-b1, version 1.0.0, lesson_count 1, description, tags).
Place it after the `python-basics-from-de` block (with the other German-source
non-language sets), or after the `en-b1-from-de` block — author's choice.

**Step D — update `README.md`**
- Add a table row (note: 1 lesson, new domain):
  `| Deutsch B1 (Wissen) | Deutsch (DE) | Deutsch (DE) | 1 | B1 | Wissen |`
- Add under the `sets/de/` tree: `│   ├── de-b1/           # Domain: Knowledge`
- Update the totals line: **330 → 331 Lektionen** (hours stay ~70).

**Step E — validate & verify**
- `python3 scripts/validate_content.py` → expect **17 set(s) passed**.
- Re-run the README reconciliation: table rows must sum to 331 and match the
  manifest's 17 sets and the stated total.

**Step F — commit (two commits) & PR**
- Commit 1: lesson fix + new set manifest.
- Commit 2: root manifest + README wiring.
- Branch off fresh `main`, open a PR; do not bundle with unrelated changes.

## 6. Alternative: discard

If a human decides this artifact shouldn't ship, the clean-up is simply:
`git rm -r sets/de/de-b1/` on a branch, commit, PR. No manifest/README changes
are needed because nothing references it today.

---

### Quick checklist for cc
- [ ] Human confirms: import vs discard; keep `domain: knowledge`.
- [ ] Fix lesson `id` → kebab slug.
- [ ] Add ≥2 `distractors` to each of the 4 `free_text` exercises (validator blocker).
- [ ] Create `sets/de/de-b1/manifest.yaml`.
- [ ] Add set block to root `manifest.yaml`.
- [ ] README: row + tree entry + totals 330→331.
- [ ] `validate_content.py` → 17 sets pass; README sums reconcile.
- [ ] Two commits, branch off main, PR.
