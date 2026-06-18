# Adaptive Learner Content

Official content repository for [Adaptive Learner](https://github.com/astrapi69/adaptive-learner).

## Content Sets

| Set | Source | Target | Lessons | Level | Domain |
|-----|--------|--------|---------|-------|--------|
| Französisch A1 | Deutsch (DE) | Französisch (FR) | 15 | A1 | Sprache |
| Französisch A2 | Deutsch (DE) | Französisch (FR) | 15 | A2 | Sprache |
| Französisch B1 | Deutsch (DE) | Französisch (FR) | 15 | B1 | Sprache |
| Französisch A1 | English (EN) | French (FR) | 15 | A1 | Language |
| Französisch A2 | English (EN) | French (FR) | 15 | A2 | Language |
| Spanisch A1 | Deutsch (DE) | Spanisch (ES) | 15 | A1 | Sprache |
| Spanisch A2 | Deutsch (DE) | Spanisch (ES) | 15 | A2 | Sprache |
| Spanisch B1 | Deutsch (DE) | Spanisch (ES) | 15 | B1 | Sprache |
| Spanisch A1 | English (EN) | Spanish (ES) | 15 | A1 | Language |
| Spanisch A2 | English (EN) | Spanish (ES) | 15 | A2 | Language |
| Spanisch B1 | English (EN) | Spanish (ES) | 15 | B1 | Language |
| Englisch A1 | Deutsch (DE) | English (EN) | 15 | A1 | Sprache |
| Englisch A2 | Deutsch (DE) | English (EN) | 15 | A2 | Sprache |
| Englisch B1 | Deutsch (DE) | English (EN) | 15 | B1 | Sprache |
| English A1 | हिंदी (HI) | English (EN) | 10 | A1 | Language |
| Deutsch A1 | English (EN) | German (DE) | 5 | A1 | Language |
| Psychologie | Deutsch (DE) | Deutsch (DE) | 112 | Uni-Intro | Psychologie |
| Python — Grundlagen | Deutsch (DE) | Deutsch (DE) | 15 | A1 | Programmierung |
| KI für Einsteiger | Deutsch (DE) | Deutsch (DE) | 12 | Einsteiger | KI |
| Japanisch A1 | Deutsch (DE) | 日本語 (JA) | 10 | A1 | Sprache |
| Koreanisch A1 | Deutsch (DE) | 한국어 (KO) | 10 | A1 | Sprache |
| Italienisch A1 | Deutsch (DE) | Italiano (IT) | 10 | A1 | Sprache |
| Portugiesisch (BR) A1 | Deutsch (DE) | Português-BR (PT) | 10 | A1 | Sprache |
| Chinesisch A1 | Deutsch (DE) | 中文 (ZH) | 10 | A1 | Sprache |
| IT-Grundlagen | Deutsch (DE) | Deutsch (DE) | 10 | Einsteiger | Technik |

**424 Lektionen · ~88 Stunden Lernmaterial**

## Directory Structure

```
sets/
├── de/                 # Source language: German
│   ├── fr-a1/          # Target: French A1
│   ├── fr-a2/          # Target: French A2
│   ├── fr-b1/          # Target: French B1
│   ├── es-a1/          # Target: Spanish A1
│   ├── es-a2/          # Target: Spanish A2
│   ├── es-b1/          # Target: Spanish B1
│   ├── en-a1/          # Target: English A1
│   ├── en-a2/          # Target: English A2
│   ├── en-b1/          # Target: English B1
│   ├── psych-intro/    # Domain: Psychology
│   ├── python-basics/  # Domain: Programming
│   ├── ki-einsteiger/  # Domain: AI
│   ├── ja-a1/          # Target: Japanese A1
│   ├── ko-a1/          # Target: Korean A1
│   ├── it-a1/          # Target: Italian A1
│   ├── pt-a1/          # Target: Brazilian Portuguese A1
│   ├── zh-a1/          # Target: Mandarin Chinese A1
│   └── it-grundlagen/  # Domain: Technology (IT fundamentals)
├── en/                 # Source language: English
│   ├── de-a1/          # Target: German A1
│   ├── fr-a1/          # Target: French A1
│   ├── fr-a2/          # Target: French A2
│   ├── es-a1/          # Target: Spanish A1
│   ├── es-a2/          # Target: Spanish A2
│   └── es-b1/          # Target: Spanish B1
├── hi/                 # Source language: Hindi
│   └── en-a1/          # Target: English A1
└── manifest.yaml       # Root manifest
```

## Schema

Content uses schema v1.2 / v1.3 with:
- `source_language` + `target_language` (language pairs)
- `domain` field for non-language content (default: `language`). For
  non-language domains (e.g. `psychology`, `programming`) the
  explanations and the material share one language, so
  `source_language == target_language` is allowed and the set folder
  carries a topic name (e.g. `sets/de/psych-intro`,
  `sets/de/python-basics`) instead of a `{target}-{level}` name.
- Schema v1.3 adds optional card fields for code content:
  `code_snippet`, `code_language`, `expected_output`, `hint`,
  `difficulty` (1–5), `media_type` (`text` | `code` | `formula` |
  `diagram`) and `tags`. When a card has `media_type: "code"`, the
  viewer renders the card and its exercises in code-aware mode
  (monospace, no spellcheck). All v1.3 fields are optional and
  backward compatible.
- 5 exercise types: Matching, Picture Choice, Free Text, Word Tiles, Cloze
- Progressive direction: receptive → mixed → productive

## Eigene Lektionen erstellen

Du willst eigene Inhalte erstellen? So gehst du vor:

1. Lies die [Schnellstart-Anleitung](docs/GETTING-STARTED.md)
2. Kopiere ein [Template](templates/) für deine Domäne (`language`, `knowledge`, `programming`)
3. Füge deine Inhalte ein (eine vollständige Beispiel-Lektion: [`examples/inception-effekt/`](examples/inception-effekt/))
4. Validiere mit `python3 scripts/validate_content.py`
5. Verbinde dein Repo in der App (Einstellungen → Inhalte) oder öffne einen Pull Request

Für die vollständige Schema-Referenz siehe [docs/LESSON-FORMAT.md](docs/LESSON-FORMAT.md).
Als forkbarer Startpunkt für ein eigenes Content-Repo dient
[adaptive-learner-content-test](https://github.com/astrapi69/adaptive-learner-content-test).

## Contributing

1. Create lessons using the [Lesson Creator](https://astrapi69.github.io/adaptive-learner/) in the app
2. Share via "Für die Community bereitstellen" — creates a PR automatically
3. Or: fork this repo, add your set under `sets/{source}/{target}-{level}/`, open a PR

See the [Content Authoring Guide](https://github.com/astrapi69/adaptive-learner/blob/main/docs/help/en/content-authoring-guide.md) for the full schema reference.

## Validation

```bash
python3 scripts/validate_content.py
```

All PRs are validated automatically via CI.

## License

Content is licensed under [CC-BY-SA-4.0](./LICENSE).
