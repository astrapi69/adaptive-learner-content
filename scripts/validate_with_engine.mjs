#!/usr/bin/env node
/**
 * Engine conformance gate: run learn-content-engine's validateLesson()
 * (structural ajv layer AND the semantic cross-field rules — cloze
 * markers == blanks, referential card_ids integrity, multiselect
 * disjointness, picture-choice exactly-one-correct, ...) over EVERY
 * lesson in this repo, plus validateManifest() over the root manifest
 * and every per-set manifest. Gate: zero errors.
 *
 * Rationale: the structural CI (validate_content.py against the
 * mirrored JSON Schema) cannot see cross-field semantics; a real
 * conformance run found two semantic bugs in the official content repo
 * that the structural gate had passed. This job closes that hole with
 * the engine's own validator — the same one third-party consumers run.
 *
 * The engine version comes from schema/engine-version.txt (the same pin
 * the schema-mirror drift gate uses); CI installs it with
 * `npm install --no-save learn-content-engine@$(cat schema/engine-version.txt)`.
 *
 * Usage:
 *   node scripts/validate_with_engine.mjs               # validate sets/
 *   node scripts/validate_with_engine.mjs --self-test   # prove the gate bites
 *   node scripts/validate_with_engine.mjs --warnings     # also list W-* lints
 *
 * --self-test feeds known-bad lessons (one per semantic rule class) to
 * validateLesson and exits non-zero unless EVERY one is rejected — so a
 * silently toothless validator cannot masquerade as a green gate.
 *
 * --warnings also lists the author lints (W-*) that never block. It runs
 * through the SAME extension registry as the error gate, so ext: lessons are
 * validated instead of refused — make lint-warnings used to shell out to the
 * bare CLI (no registry) and died on ext content (content-test#71).
 */
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { validateLesson, validateManifest } from "learn-content-engine";
import { parse as parseYaml } from "yaml";

const repoRoot = fileURLToPath(new URL("..", import.meta.url));
const setsDir = join(repoRoot, "sets");

// --- adopted extension tier (content-test#66) ------------------------------
// The app has ADOPTED these ext: types - a mirror of its SUPPORTED_EXTENSIONS
// (frontend/src/lib/content/validation/lesson-schema-validator.ts). Registering
// them lets a lesson that DECLARES one load through this gate instead of being
// refused (E-EXT-UNSUPPORTED), while any UNADOPTED ext type is still refused -
// exactly the app's load-guard contract, applied at content-CI time.
//
// The validators are permissive on purpose: ext_payload CORRECTNESS is the
// consumer's job (the app's validateGeneratedLesson owns the payload rules).
// Publishing those rules so this gate can reuse them - instead of vendoring a
// drift-prone copy - is the follow-up. Keep this list in sync with the app
// when a new extension is adopted.
const ADOPTED_EXTENSIONS = [
  "ext:al-categorization",
  "ext:al-error-correction",
  "ext:al-reading-comprehension",
  "ext:al-graded-quiz",
].map((type) => ({ type, major: 1, validate: () => [] }));

const withExtensions = { extensions: ADOPTED_EXTENSIONS };

function collectLessonFiles(dir) {
  const files = [];
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) files.push(...collectLessonFiles(full));
    else if (entry.endsWith(".json")) files.push(full);
  }
  return files.sort();
}

function collectManifestFiles() {
  // The root manifest plus every per-set manifest — all must conform to
  // the engine's (strict) content-manifest schema.
  const files = [join(repoRoot, "manifest.yaml")];
  for (const entry of readdirSync(setsDir)) {
    const langDir = join(setsDir, entry);
    if (!statSync(langDir).isDirectory()) continue;
    for (const setEntry of readdirSync(langDir)) {
      const manifest = join(langDir, setEntry, "manifest.yaml");
      try {
        if (statSync(manifest).isFile()) files.push(manifest);
      } catch {
        /* set dir without manifest — validate_content.py reports that */
      }
    }
  }
  return files.sort();
}

// One minimal valid lesson the bad cases are derived from; each bad case
// violates exactly one semantic rule the engine must flag.
const baseLesson = () => ({
  id: "self-test",
  title: "Self test",
  cards: [{ id: "c1", front: "a", back: "b" }],
  steps: [
    { id: "t1", type: "theory", title: "T", body: "Theory." },
    {
      id: "e1",
      type: "exercise",
      theory_ref: "t1",
      title: "E",
      exercise: {
        id: "e1",
        type: "cloze",
        prompt: "Fill in.",
        card_ids: ["c1"],
        sentence: "One ___ here.",
        blanks: [{ accept: ["blank"] }],
        cloze_mode: "type",
      },
    },
  ],
});

const SELF_TEST_CASES = [
  {
    name: "cloze marker/blank count mismatch",
    mutate(lesson) {
      lesson.steps[1].exercise.sentence = "Two ___ markers ___ here.";
    },
  },
  {
    name: "card_ids referential integrity",
    mutate(lesson) {
      lesson.steps[1].exercise.card_ids = ["no-such-card"];
    },
  },
  {
    name: "multiselect accept/distractors disjointness",
    mutate(lesson) {
      lesson.steps[1].exercise = {
        id: "e1",
        type: "cloze",
        prompt: "Pick all.",
        card_ids: ["c1"],
        sentence: "Pick ___ now.",
        cloze_mode: "multiselect",
        accept: ["same"],
        distractors: ["same", "other"],
      };
    },
  },
  {
    name: "picture_choice exactly-one-correct",
    mutate(lesson) {
      lesson.steps[1].exercise = {
        id: "e1",
        type: "picture_choice",
        prompt: "Which one?",
        card_ids: ["c1"],
        images: [
          { src: "a.png", alt: "a", is_correct: "true" },
          { src: "b.png", alt: "b", is_correct: "true" },
        ],
      };
    },
  },
  {
    name: "structural: unknown field rejected",
    mutate(lesson) {
      lesson.totally_unknown_field = true;
    },
  },
];

// Manifest self-test: the strict set entry must reject unknown fields
// (the ai_validation-in-set-entry class); free-form metadata must pass.
const MANIFEST_SELF_TEST = () => {
  const base = {
    schema_version: "1.0",
    name: "Self test",
    sets: [
      {
        id: "self-test",
        title: "Self test",
        target_language: "de",
        source_language: "en",
        level: "A1",
        path: "sets/en/de-a1",
        version: "1.0.0",
        lesson_count: 1,
      },
    ],
    metadata: { free_form: true },
  };
  const good = validateManifest(base);
  const bad = structuredClone(base);
  bad.sets[0].totally_unknown_field = true;
  const rejected = validateManifest(bad);
  return { good, rejected };
};

/** A base lesson whose exercise is replaced by an ``ext:`` one. */
function extLesson(type, extPayload) {
  const lesson = baseLesson();
  lesson.requires_extensions = [`${type}@1`];
  lesson.steps[1].exercise = {
    id: "e1",
    type,
    prompt: "Ext exercise.",
    card_ids: ["c1"],
    ext_payload: extPayload,
  };
  return lesson;
}

function selfTest() {
  const sane = validateLesson(baseLesson(), withExtensions);
  if (!sane.valid) {
    console.error("SELF-TEST BROKEN: the base lesson must be valid:");
    for (const issue of sane.errors) console.error(`   ${issue.path}: ${issue.message}`);
    return 1;
  }
  let failures = 0;
  for (const testCase of SELF_TEST_CASES) {
    const lesson = baseLesson();
    testCase.mutate(lesson);
    const result = validateLesson(lesson, withExtensions);
    if (result.valid) {
      failures++;
      console.error(`SELF-TEST FAIL: engine did not flag: ${testCase.name}`);
    } else {
      console.log(`self-test OK: ${testCase.name}`);
    }
  }
  const { good, rejected } = MANIFEST_SELF_TEST();
  if (!good.valid) {
    failures++;
    console.error("SELF-TEST BROKEN: the base manifest must be valid:");
    for (const issue of good.errors) console.error(`   ${issue.path}: ${issue.message}`);
  } else if (rejected.valid) {
    failures++;
    console.error("SELF-TEST FAIL: engine did not flag: unknown field in strict manifest set entry");
  } else {
    console.log("self-test OK: unknown field in strict manifest set entry");
  }

  // Extension tier (content-test#66): an ADOPTED ext type loads, an UNADOPTED
  // one is still refused loudly.
  const adopted = validateLesson(
    extLesson("ext:al-categorization", {
      categories: [
        { name: "A", items: ["x"] },
        { name: "B", items: ["y"] },
      ],
    }),
    withExtensions,
  );
  if (!adopted.valid) {
    failures++;
    console.error("SELF-TEST FAIL: an adopted extension lesson must load:");
    for (const issue of adopted.errors) console.error(`   ${issue.path}: ${issue.message}`);
  } else {
    console.log("self-test OK: adopted extension ext:al-categorization loads");
  }

  const gradedQuiz = validateLesson(
    extLesson("ext:al-graded-quiz", {
      pass_threshold: 60,
      questions: [
        { prompt: "2+2?", type: "multiple_choice", options: [{ text: "4", correct: true }, { text: "5" }], points: 2 },
      ],
    }),
    withExtensions,
  );
  if (!gradedQuiz.valid) {
    failures++;
    console.error("SELF-TEST FAIL: an adopted ext:al-graded-quiz lesson must load:");
    for (const issue of gradedQuiz.errors) console.error(`   ${issue.path}: ${issue.message}`);
  } else {
    console.log("self-test OK: adopted extension ext:al-graded-quiz loads");
  }

  const unadopted = validateLesson(extLesson("ext:zz-unknown", {}), withExtensions);
  if (unadopted.valid) {
    failures++;
    console.error("SELF-TEST FAIL: an unadopted extension must be refused (E-EXT-UNSUPPORTED)");
  } else {
    console.log("self-test OK: unadopted extension ext:zz-unknown refused");
  }

  // Warning tier (content-test#71): author lints (W-*) are surfaced but never
  // block. Proves the --warnings path is not toothless and that ext lessons
  // reach the warning check instead of erroring out. A lesson with an unused
  // card stays valid AND carries a W-CARD-UNUSED warning.
  const warnLesson = baseLesson();
  warnLesson.cards.push({ id: "c-unused", front: "orphan", back: "never referenced" });
  const warned = validateLesson(warnLesson, withExtensions);
  if (!warned.valid) {
    failures++;
    console.error("SELF-TEST BROKEN: an unused-card lesson must stay valid (warning, not error):");
    for (const issue of warned.errors) console.error(`   ${issue.path}: ${issue.message}`);
  } else if (!warned.warnings.some((issue) => issue.id === "W-CARD-UNUSED")) {
    failures++;
    console.error("SELF-TEST FAIL: expected a surfaced W-CARD-UNUSED warning, got none");
  } else {
    console.log("self-test OK: author-lint warning surfaced (W-CARD-UNUSED)");
  }

  if (failures) return 1;
  console.log(`\nSelf-test passed: the gate rejects all ${SELF_TEST_CASES.length + 1} bad-input classes, gates the extension tier, and surfaces author warnings.`);
  return 0;
}

// With `showWarnings`, the author lints (W-*) are ALSO listed. Warnings never
// change the exit code (errors-only), so `make lint-warnings` is a reporter,
// not a gate. It runs through the SAME extension registry as the error gate,
// so an ext: lesson is validated (not refused with E-EXT-UNSUPPORTED) - the bug
// this replaces used the bare CLI without a registry (content-test#71).
function validateAll({ showWarnings = false } = {}) {
  const files = collectLessonFiles(setsDir);
  let invalid = 0;
  const warned = [];
  for (const file of files) {
    let lesson;
    try {
      lesson = JSON.parse(readFileSync(file, "utf8"));
    } catch (error) {
      invalid++;
      console.error(`PARSE ERROR ${file}: ${error.message}`);
      continue;
    }
    const result = validateLesson(lesson, withExtensions);
    if (!result.valid) {
      invalid++;
      console.error(`INVALID ${file.slice(repoRoot.length)}`);
      for (const issue of result.errors) console.error(`   ${issue.path}: ${issue.message}`);
    }
    if (showWarnings && result.warnings.length) {
      warned.push({ file: file.slice(repoRoot.length), warnings: result.warnings });
    }
  }
  const manifests = collectManifestFiles();
  for (const file of manifests) {
    let doc;
    try {
      doc = parseYaml(readFileSync(file, "utf8"));
    } catch (error) {
      invalid++;
      console.error(`PARSE ERROR ${file}: ${error.message}`);
      continue;
    }
    const result = validateManifest(doc);
    if (!result.valid) {
      invalid++;
      console.error(`INVALID ${file.slice(repoRoot.length)}`);
      for (const issue of result.errors) console.error(`   ${issue.path}: ${issue.message}`);
    }
  }
  const totalWarnings = warned.reduce((sum, w) => sum + w.warnings.length, 0);
  console.log(
    `\n${files.length} lesson(s) + ${manifests.length} manifest(s) checked ` +
      `with the engine validator, ${invalid} invalid` +
      (showWarnings ? `, ${totalWarnings} warning(s)` : "") +
      ".",
  );
  if (showWarnings) {
    for (const w of warned) {
      console.log(`\nWARN ${w.file}`);
      for (const issue of w.warnings) console.log(`   [${issue.id}] ${issue.path} ${issue.message}`);
    }
  }
  return invalid ? 1 : 0;
}

const args = process.argv.slice(2);
if (args.includes("--self-test")) {
  process.exit(selfTest());
}
process.exit(validateAll({ showWarnings: args.includes("--warnings") }));
