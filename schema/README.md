# Schema (mirror — do not edit here)

These files are **mirrored from the app repository
[`astrapi69/adaptive-learner`](https://github.com/astrapi69/adaptive-learner)**
and are the App-authoritative definition of the lesson format (EXP-039).

> ⚠️ **Do not hand-edit these files in this repo.** They are byte-for-byte
> copies of the app's generated artefacts. The single source of truth is the
> Pydantic model in `adaptive_learner_content_loader.schema` in the app repo,
> from which `make sync-schema` (`scripts/generate_lesson_schema.py`)
> regenerates them. Edit the model there and re-run the generator — then update
> this mirror.

## What is mirrored

| File | Origin (app repo, `master`) | Consumed here by |
|------|-----------------------------|------------------|
| `lesson.schema.json` | `schema/lesson.schema.json` | `scripts/validate_content.py` (structural validation via `jsonschema`) |
| `quality-rules.json` | `schema/quality-rules.json` | `scripts/validate_content.py` (quality minimums) |

`lesson.schema.json` is a self-contained JSON Schema (Draft 2020-12) — its
`$id`, `$schema` and `x-schema-version` make it usable for IDE autocomplete
(reference it from a lesson `.json` via `"$schema"`) and for `jsonschema`/`ajv`
validation. `quality-rules.json` carries the shared quality minimums
(`minExercisesPerLesson`, `minExerciseTypes`, `minFreeTextAccepts`,
`minMatchingPairs`, `minTheorySteps`) that both the app and this repo read, so
the numbers never drift apart.

## Drift gate

`scripts/check_schema_drift.py` (run in CI by
`.github/workflows/schema-drift.yml`) downloads the originals from the app repo
at CI time and compares them byte-for-byte against this mirror. If the app side
changes a schema, this check goes **red** until the mirror is refreshed — a
schema change in the app gets a visible consequence here instead of silent
drift.

To refresh the mirror after an app-side schema change:

```bash
python scripts/check_schema_drift.py --update   # pulls the latest app artefacts
git add schema/ && git commit -m "schema: refresh mirror from adaptive-learner"
```

This is the same cross-repo philosophy the app already uses in the other
direction: the app repo holds this repo's CI contract under
`docs/ci/adaptive-learner-content/`. App is the source; the partner repo keeps a
marked copy plus a drift gate.
