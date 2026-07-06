# Lesson format — schema reference (moved)

> ℹ️ **The authoritative lesson-format reference now lives in the
> learn-content-engine repository.** This repo no longer keeps a parallel
> copy that could drift.

The lesson format is canonical along the chain **adaptive-learner Pydantic →
[`learn-content-engine`](https://github.com/astrapi69/learn-content-engine) →
this mirror**: the schema is generated from the app's Pydantic model, vendored
by the engine per its documented sync procedure, and mirrored here pinned to
the engine version in [`schema/engine-version.txt`](../schema/engine-version.txt).
This content repo only **mirrors** the machine-readable schema and follows
it — it does not define or extend the format.

## Where the real reference is

- **Format reference with a tested example per exercise type:**
  [`learn-content-engine/docs/lesson-format.md`](https://github.com/astrapi69/learn-content-engine/blob/main/docs/lesson-format.md)
- **Machine-readable JSON Schema (mirrored into this repo, pinned):**
  [`schema/lesson.schema.json`](../schema/lesson.schema.json) — Draft 2020-12,
  `x-schema-version: 1.5`; also importable as
  `learn-content-engine/schema/lesson.schema.json` from the npm package.
  Reference it from a lesson `.json` via `"$schema"` for IDE autocomplete +
  validation. See [`schema/README.md`](../schema/README.md) for how the
  mirror and its drift gate work.
- **Shared quality minimums:** [`schema/quality-rules.json`](../schema/quality-rules.json)
  (`minExercisesPerLesson`, `minExerciseTypes`, `minFreeTextAccepts`,
  `minMatchingPairs`, `minTheorySteps`).
- **Which exercise type for which learning goal (didactic guideline, EXP-041):**
  the schema tells you the *shape* of each type, not *when* to use it. Choose the
  type by learning goal — facts/definitions as `cloze` (or multiple choice via
  `cloze` `select` mode), `word_tiles` only for sentences with one unambiguous
  word order, and never exact-match grading for free production (it red-marks a
  content-correct learner). Full guideline in the app authoring guide:
  English — <https://astrapi69.github.io/adaptive-learner/docs/en/developer/authoring-content/>
  · Deutsch — <https://astrapi69.github.io/adaptive-learner/docs/de/developer/authoring-content/>

## Validating your content here

`scripts/validate_content.py` validates the structural fields **against the
mirrored `schema/lesson.schema.json`** (via the `jsonschema` library), reads the
quality minimums from `schema/quality-rules.json`, and adds the content-repo
specifics (ISO 639-1 language pair, source-language directory layout, non-Latin
script checks, distractor minimums, `word_tiles` ordering permutation).

```bash
pip install "pyyaml>=6,<7" "jsonschema>=4,<5"
python scripts/validate_content.py     # until it prints "All N set(s) passed validation."
```

## Getting started

New here? Start with [GETTING-STARTED.md](GETTING-STARTED.md) and copy a
[template](../templates/). Then consult the generated reference above for the
exact fields.
