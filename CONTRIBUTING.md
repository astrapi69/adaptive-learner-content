# Beitragen zu Adaptive Learner Content

Danke für dein Interesse! So kannst du beitragen:

## Neues Set erstellen

1. Fork dieses Repo
2. Erstelle einen Ordner unter `sets/{source_lang}/{target_lang}-{level}/`
   (für Nicht-Sprach-Domains einen Themennamen, z. B. `sets/de/adaptive-learner-app/`)
3. Erstelle `manifest.yaml` (siehe bestehendes Set als Vorlage)
4. Erstelle Lektionen als JSON unter `lessons/`
5. Pull Request öffnen

## Bestehendes Set verbessern

- Fehler in Übersetzungen? → Issue erstellen oder PR
- Fehlende Übungen? → Neue Exercises hinzufügen
- Native-Speaker Review? → Kommentar am Set

## Qualitäts-Richtlinien

- Alle Texte müssen sprachlich korrekt sein
- Exercises müssen abwechslungsreich sein (nicht nur Matching)
- Metadaten (Level, Domain, Tags) müssen stimmen
- Keine urheberrechtlich geschützten Inhalte

## Review-Prozess

1. PR öffnen mit Beschreibung der Änderungen
2. Automatische KI-Validierung läuft (`python3 scripts/validate_content.py`)
3. Manueller Review durch Maintainer
4. Merge nach Approval
