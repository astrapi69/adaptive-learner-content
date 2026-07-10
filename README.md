# Adaptive Learner Content

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
> **30 Sets, 452 Lektionen, 5566 Karten** in 10 Sprachen.
> Sprachen lernen, KI verstehen, Ansible meistern.
> Spaced-Repetition-optimiert, KI-validiert, CC-BY-SA-4.0.

> Free, open **language- and knowledge-learning content** for
> [Adaptive Learner](https://astrapi69.github.io/adaptive-learner/) -
> **30 sets, 452 lessons, 5566 cards** across 10 languages.
> Learn French, Spanish, English, Japanese, Korean, Chinese,
> Italian, Portuguese - plus German, AI fundamentals and DevOps.
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
| KI für Einsteiger | DE | Einsteiger | 12 | 144 | KI | ✓ Validiert |
| Psychologie Einführung | DE | Uni-Intro | 112 | 1408 | Psychologie | Review |
| Python Grundlagen | DE | Einsteiger | 15 | 166 | Programmierung | Review |
| IT-Grundlagen | DE | Einsteiger | 10 | 115 | Technik | Review |
| Ansible QE | DE | B1 | 8 | 88 | DevOps | Review |
| Data Science und KI | DE | A2 | 9 | 72 | KI | Review |
| Adaptive Learner — App-Tutorial | DE | Einsteiger | 12 | 95 | App-Tutorial | Review |

**Gesamt: 35 Sets, 499 Lektionen, 5919 Karten in 10 Sprachen.**

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
    ki-einsteiger/       # Domain: KI
    psych-intro/         # Domain: Psychologie
    python-basics/       # Domain: Programmierung
    it-grundlagen/       # Domain: Technik
    ansible-qe/          # Domain: DevOps
    ...
  en/                    # Quellsprache: Englisch
    fr-a1/  es-a1/  de-a1/  ...
  hi/                    # Quellsprache: Hindi
    en-a1/               # Ziel: Englisch A1
  manifest.yaml          # Root-Manifest
```

### Manifest- und Lektions-Format

Das Feld-Schema (Root- und Set-`manifest.yaml`, alle Lektions- und
Aufgaben-Felder, die fünf Aufgabentypen und die drei cloze-Modi) wird hier
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

> Für Nicht-Sprach-Domains (z. B. `psychology`, `programming`) teilen sich
> Erklärung und Material eine Sprache, d. h. `source_language == target_language`
> ist erlaubt und der Ordner trägt einen Themennamen
> (z. B. `sets/de/psych-intro`).

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
[docs/CROSS-REPO-SEARCH.md](docs/CROSS-REPO-SEARCH.md) — die Kurzanleitung
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
- **Teilen** - das Material kopieren und weiterverbreiten
- **Anpassen** - das Material verändern und darauf aufbauen
- **Kommerziell nutzen** - auch für kommerzielle Zwecke

Unter folgenden Bedingungen:
- **Namensnennung** - angemessene Credits geben
- **Weitergabe unter gleichen Bedingungen** - gleiche Lizenz verwenden

---

## Links

- [Adaptive Learner App](https://astrapi69.github.io/adaptive-learner/) - Die Lern-App
- [Adaptive Learner Repo](https://github.com/astrapi69/adaptive-learner) - App Source Code
- [docker-app-launcher](https://github.com/astrapi69/docker-app-launcher) - Desktop Launcher
- [Lesson-Format-Referenz](https://github.com/astrapi69/learn-content-engine/blob/main/docs/lesson-format.md) - Technische Format-Dokumentation (learn-content-engine; Schema-Spiegel siehe [schema/README.md](schema/README.md))
- [Cross-Repo-Suche & eigenes Repo eintragen](docs/CROSS-REPO-SEARCH.md) - Wie die Suche über mehrere Content-Repos funktioniert und wie du deins anmeldest
- [CONTRIBUTING.md](CONTRIBUTING.md) - Mitmachen und Inhalte beitragen
