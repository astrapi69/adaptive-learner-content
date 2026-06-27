# Lesson format — schema reference (moved)

> ℹ️ **The authoritative lesson-format reference now lives in the app
> repository.** This repo no longer keeps a parallel copy that could drift.

The lesson format is **App-authoritative** (EXP-039): it is generated from the
Pydantic model in the [`astrapi69/adaptive-learner`](https://github.com/astrapi69/adaptive-learner)
app and published as a single source of truth. This content repo only
**mirrors** the machine-readable schema and follows it — it does not define or
extend the format.

## Where the real reference is

- **Field-by-field reference (generated docs):**
  - English — <https://astrapi69.github.io/adaptive-learner/docs/en/developer/lesson-format-reference/>
  - Deutsch — <https://astrapi69.github.io/adaptive-learner/docs/de/developer/lesson-format-reference/>
  - Source (always current):
    [`docs/help/en/developer/lesson-format-reference.md`](https://github.com/astrapi69/adaptive-learner/blob/master/docs/help/en/developer/lesson-format-reference.md)
- **Machine-readable JSON Schema (mirrored into this repo):**
  [`schema/lesson.schema.json`](../schema/lesson.schema.json) — Draft 2020-12,
  `x-schema-version: 1.4`. Reference it from a lesson `.json` via `"$schema"` for
  IDE autocomplete + validation. See [`schema/README.md`](../schema/README.md)
  for how the mirror and its drift gate work.
- **Shared quality minimums:** [`schema/quality-rules.json`](../schema/quality-rules.json)
  (`minExercisesPerLesson`, `minExerciseTypes`, `minFreeTextAccepts`,
  `minMatchingPairs`, `minTheorySteps`).

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
