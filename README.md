# Adaptive Learner Content

[![content validation](https://github.com/astrapi69/adaptive-learner-content/actions/workflows/validate-content.yml/badge.svg)](https://github.com/astrapi69/adaptive-learner-content/actions/workflows/validate-content.yml)
[![engine on npm](https://img.shields.io/npm/v/learn-content-engine?label=engine%20on%20npm)](https://www.npmjs.com/package/learn-content-engine)
[![Sets](https://img.shields.io/badge/sets-35-0d9488)](#content-sets)
[![Lessons](https://img.shields.io/badge/lessons-499-0d9488)](#content-sets)
[![Cards](https://img.shields.io/badge/cards-5919-0d9488)](#content-sets)
[![Languages](https://img.shields.io/badge/languages-10-0d9488)](#content-sets)
[![Hours](https://img.shields.io/badge/~88h-learning%20content-0d9488)](#content-sets)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/license-CC--BY--SA--4.0-blue)](LICENSE)
[![AI Validated](https://img.shields.io/badge/AI-validated-green)](#qualität)
[![Open in Adaptive Learner](https://img.shields.io/badge/%E2%96%B6%20Open%20in-Adaptive%20Learner-0d9488)](https://astrapi69.github.io/adaptive-learner/)

> **Kostenlose, offene Lerninhalte** für
> [Adaptive Learner](https://astrapi69.github.io/adaptive-learner/) -
> **28 Sets, 325 Lektionen, 3877 Karten** in 10 Sprachen.
> Sprachen lernen, die App meistern.
> Spaced-Repetition-optimiert, KI-validiert, CC-BY-SA-4.0.

> Free, open **language- and knowledge-learning content** for
> [Adaptive Learner](https://astrapi69.github.io/adaptive-learner/) -
> **28 sets, 325 lessons, 3877 cards** across 10 languages.
> Learn French, Spanish, English, Japanese, Korean, Chinese,
> Italian, Portuguese, plus German and the app tutorial.
> Spaced-repetition-ready, AI-validated, CC-BY-SA-4.0.

---

## Schnellstart

### Im Browser (keine Installation)

1. [Adaptive Learner öffnen](https://astrapi69.github.io/adaptive-learner/)
2. **Inhalte** → **Entdecken** → Set auswählen → **Herunterladen**
3. Lernen!

### Als eigene Content-Quelle

```bash
# In Adaptive Learner:
# Einstellungen → Integrationen → Repository hinzufügen
# URL: https://github.com/astrapi69/adaptive-learner-content
```

### Für Entwickler

```bash
git clone https://github.com/astrapi69/adaptive-learner-content.git
cd adaptive-learner-content
# Jedes Set ist ein Ordner unter sets/
ls sets/
```

---

## Content-Sets

| Set | Sprache | Level | Lektionen | Karten | Domain | Status |
|-----|---------|-------|-----------|--------|--------|--------|
| Französisch A1 | DE→FR | A1 | 15 | 186 | Sprache | Review |
| Französisch A2 | DE→FR | A2 | 15 | 180 | Sprache | Review |
| Französisch B1 | DE→FR | B1 | 15 | 193 | Sprache | Review |
| Spanisch A1 | DE→ES | A1 | 15 | 230 | Sprache | Review |
| Spanisch A2 | DE→ES | A2 | 15 | 182 | Sprache | Review |
| Spanisch B1 | DE→ES | B1 | 15 | 197 | Sprache | Review |
| Englisch A1 | DE→EN | A1 | 15 | 163 | Sprache | Review |
| Englisch A2 | DE→EN | A2 | 15 | 182 | Sprache | Review |
| Englisch B1 | DE→EN | B1 | 15 | 188 | Sprache | Review |
| Japanisch A1 | DE→JA | A1 | 10 | 122 | Sprache | Review |
| Koreanisch A1 | DE→KO | A1 | 10 | 119 | Sprache | Review |
| Chinesisch A1 | DE→ZH | A1 | 10 | 122 | Sprache | Review |
| Italienisch A1 | DE→IT | A1 | 10 | 125 | Sprache | Review |
| Portugiesisch-BR A1 | DE→PT | A1 | 10 | 130 | Sprache | Review |
| Französisch A1 | EN→FR | A1 | 15 | 190 | Sprache | Review |
| Französisch A2 | EN→FR | A2 | 15 | 178 | Sprache | Review |
| Französisch B1 | EN→FR | B1 | 5 | 37 | Sprache | Review |
| Spanisch A1 | EN→ES | A1 | 15 | 253 | Sprache | Review |
| Spanisch A2 | EN→ES | A2 | 15 | 179 | Sprache | Review |
| Spanisch B1 | EN→ES | B1 | 15 | 179 | Sprache | Review |
| Spanisch B2 | EN→ES | B2 | 5 | 36 | Sprache | Review |
| Deutsch A1 | EN→DE | A1 | 5 | 66 | Sprache | Review |
| Deutsch A2 | EN→DE | A2 | 5 | 46 | Sprache | Review |
| Englisch A1 | HI→EN | A1 | 10 | 120 | Sprache | Review |
| Englisch A2 | HI→EN | A2 | 5 | 42 | Sprache | Review |
| Adaptive Learner — App-Tutorial | DE | Einsteiger | 12 | 95 | App-Tutorial | Review |

**Gesamt: 28 Sets, 325 Lektionen, 3877 Karten in 10 Sprachen.**

> Sprachen / Languages: Deutsch, Englisch, Französisch, Spanisch,
> Italienisch, Portugiesisch, Japanisch, Koreanisch, Chinesisch, Hindi.

---

## Qualität

### KI-Validierung
Jedes Set durchläuft eine automatische Qualitätsprüfung:
- Sprachliche Korrektheit
- Konsistenz der Übersetzungen
- Vollständigkeit der Metadaten
- Exercise-Typ-Balance

Alle Pull Requests werden zusätzlich in der CI automatisch validiert
(`python3 scripts/validate_content.py`).

**Vor dem Push** das Engine-Gate lokal laufen lassen: dieselben
semantischen Regeln (`E-CARD-REF`, Cloze-Marker, Multiple-Choice-Regeln),
die sonst erst die CI meldet:

```bash
make lint
```

Der erste Lauf installiert die in `schema/engine-version.txt` gepinnte
Engine lokal nach `node_modules/` (gitignored; braucht Node.js und npm),
danach laufen Selbsttest und der volle Engine-Lauf wie im CI-Workflow
`Engine validate`. Optional gibt `make lint-warnings` die Warnungen
(`W-*`) des Engine-Gates über alle Lektionen aus.

### Set-Export für KI-Review

`scripts/export_set.py` schreibt alle Lektionen EINES Sets in eine
einzige YAML- (oder JSON-) Datei, damit ein KI-Assistent oder ein Mensch
das ganze Set in einem Durchgang prüfen kann (Syntax, Korrektheit,
Konsistenz über die Lektionen hinweg):

```bash
python3 scripts/export_set.py adaptive-learner-app
# -> exports/adaptive-learner-app-de-<timestamp>.yaml
python3 scripts/export_set.py fr-a1 --lang en --format json --out /tmp/review.json
```

Der Slug ist die Set-Id aus dem Wurzel-`manifest.yaml`
(`adaptive-learner-app-from-de`) oder der Ordnername des Set-Pfads (`adaptive-learner-app`);
bei gleichnamigen Ordnern unter mehreren Quellsprachen (z. B. `fr-a1`
unter `sets/en`, `sets/de`, `sets/el`) entscheidet `--lang` (Default
`de`). Umlaute bleiben echtes UTF-8. Ein unbekannter Slug bricht mit
einer Liste der verfügbaren Sets ab.

Der Export ist selbsttragend: das erste Feld `review_instructions`
enthält den kompletten Review-Prompt aus
[`docs/ai-review-prompt-template.md`](docs/ai-review-prompt-template.md)
(zur Laufzeit gelesen, nicht im Skript kopiert). Die Exportdatei kann
also direkt und ohne manuell vorangestellten Prompt an eine Review-KI
gegeben werden. Änderungen an der Review-Anweisung in der Template-Datei
vornehmen und in den Geschwister-Content-Repos synchron halten.

**Nur-Lese-Snapshot, KEIN Re-Import-Format:** Der Export wird nirgends
zurückgelesen. Änderungen fließen ausschließlich über die einzelnen
schema-validierten Lektions-JSONs unter `sets/` ein. Der Ordner
`exports/` ist gitignored.

Ausführliche Anleitung und Best Practices (u. a. Quellkapitel-Workflow):
[`docs/export-set-usage.de.md`](docs/export-set-usage.de.md) (Deutsch) /
[`docs/export-set-usage.md`](docs/export-set-usage.md) (English).

### Status-Legende
- **✓ Validiert**: KI-geprüft + manuell gesichtet (`ai_validated: true`)
- **Review**: Kuratierter Inhalt, wartet auf KI-Validierung und Native-Speaker Review
- **Draft**: In Arbeit

### Eigene Inhalte beitragen
Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für das Content-Format
und den Review-Prozess.

---

## Content-Format

Jedes Set ist ein Ordner mit einer definierten Struktur:

```
sets/
  de/                    # Quellsprache: Deutsch
    fr-a1/               # Ziel: Französisch A1
      manifest.yaml      # Set-Metadaten
      lessons/
        01-begruessung.json
        02-zahlen.json
        ...
      media.yaml         # optional
    es-a1/               # Ziel: Spanisch A1
    en-a1/               # Ziel: Englisch A1
    ja-a1/               # Ziel: Japanisch A1
    ko-a1/               # Ziel: Koreanisch A1
    zh-a1/               # Ziel: Chinesisch A1
    it-a1/               # Ziel: Italienisch A1
    pt-a1/               # Ziel: Portugiesisch-BR A1
    ...
  en/                    # Quellsprache: Englisch
    fr-a1/  es-a1/  de-a1/  ...
  hi/                    # Quellsprache: Hindi
    en-a1/               # Ziel: Englisch A1
  manifest.yaml          # Root-Manifest
```

### Manifest- und Lektions-Format

Das Feld-Schema (Root- und Set-`manifest.yaml`, alle Lektions- und
Aufgaben-Felder, die sechs Aufgabentypen und die drei cloze-Modi) wird hier
**nicht dupliziert**. Es ist die kanonische Engine-Referenz:

- [learn-content-engine, Lesson format reference](https://github.com/astrapi69/learn-content-engine/blob/main/docs/lesson-format.md)
  (die technische Format-Dokumentation, testvalidiert, ohne App-Checkout)
- das gespiegelte, gepinnte JSON-Schema in [`schema/`](schema/) (Version in
  [`schema/engine-version.txt`](schema/engine-version.txt))

Das Schema in diesem Repo ist ein Spiegel des `learn-content-engine`-Release
(Quell-Kette: engine (kanonisch), dann dieser Spiegel).
Jede Lektion und jedes Manifest werden im CI vom gepinnten Engine-Validator
geprüft (Workflow `Engine validate`, plus die strukturelle Schema-Validierung),
sodass "validiert gegen die Engine" und "lädt in
[Adaptive Learner](https://github.com/astrapi69/adaptive-learner)" dieselbe
Aussage sind.

> Für Nicht-Sprach-Domains (z. B. `software`) teilen sich
> Erklärung und Material eine Sprache, d. h. `source_language == target_language`
> ist erlaubt und der Ordner trägt einen Themennamen
> (z. B. `sets/de/adaptive-learner-app`).

---

## Für Coaches und Lehrer

### Eigenes Content-Repo erstellen

1. Dieses Repo als Vorlage forken
2. Eigene Sets erstellen (gleiches Format)
3. In Adaptive Learner als Content-Quelle hinzufügen
4. Mit Schülern teilen via:
   - Öffentliches Repo: Link teilen
   - Privates Repo: Einladungscodes generieren

Als forkbarer Startpunkt dient
[adaptive-learner-content-test](https://github.com/astrapi69/adaptive-learner-content-test).

### In die Repo-übergreifende Suche aufnehmen

Adaptive Learner sucht über **mehrere** Content-Repos hinweg. Dein eigenes
Repo kommt hinein, indem du einen Pull Request gegen `recommended-repos.json`
öffnest, der es an einem validierten Commit anmeldet. Wie das genau
funktioniert (Datenfluss, Trust-Level, Pinning, Schritt für Schritt):
[docs/CROSS-REPO-SEARCH.md](docs/CROSS-REPO-SEARCH.md). Die Kurzanleitung
zum Eintragen steht in [docs/REGISTER-A-REPO.md](docs/REGISTER-A-REPO.md).

### Einladungscodes
Adaptive Learner unterstützt Einladungscodes für
private Content-Repos. Coaches können:
- Codes mit Limits generieren (max. Einlösungen, Ablaufdatum)
- Codes per Link, QR-Code oder manuell teilen
- Nutzung verfolgen

Mehr: [Adaptive Learner Docs](https://github.com/astrapi69/adaptive-learner)

---

## Lizenz

Alle Inhalte stehen unter
[Creative Commons Attribution-ShareAlike 4.0 International](LICENSE)
(CC-BY-SA-4.0).

Du darfst:
- **Teilen**: das Material kopieren und weiterverbreiten
- **Anpassen**: das Material verändern und darauf aufbauen
- **Kommerziell nutzen**: auch für kommerzielle Zwecke

Unter folgenden Bedingungen:
- **Namensnennung**: angemessene Credits geben
- **Weitergabe unter gleichen Bedingungen**: gleiche Lizenz verwenden

---

## Links

- [Adaptive Learner App](https://astrapi69.github.io/adaptive-learner/): Die Lern-App
- [Adaptive Learner Repo](https://github.com/astrapi69/adaptive-learner): App Source Code
- [docker-app-launcher](https://github.com/astrapi69/docker-app-launcher): Desktop Launcher
- [Lesson-Format-Referenz](https://github.com/astrapi69/learn-content-engine/blob/main/docs/lesson-format.md): Technische Format-Dokumentation (learn-content-engine; Schema-Spiegel siehe [schema/README.md](schema/README.md))
- [Cross-Repo-Suche & eigenes Repo eintragen](docs/CROSS-REPO-SEARCH.md): Wie die Suche über mehrere Content-Repos funktioniert und wie du deins anmeldest
- [CONTRIBUTING.md](CONTRIBUTING.md): Mitmachen und Inhalte beitragen
