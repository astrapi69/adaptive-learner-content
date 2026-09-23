# Makefile für das lokale Engine-Gate (dieselben Regeln wie die CI).
#
#     make lint            Installiert die gepinnte Engine (einmalig, lokal in
#                          node_modules/, per .gitignore ausgeschlossen) und
#                          lässt den Selbsttest plus den vollen Engine-Lauf
#                          über alle Lektionen und Manifeste laufen -
#                          dieselben Regel-IDs (E-CARD-REF & Co.) wie der
#                          CI-Workflow "Engine validate"
#                          (.github/workflows/engine-validate.yml), nur VOR
#                          dem Push statt danach.
#     make lint-warnings   Optional: derselbe Engine-Lauf, zusätzlich mit den
#                          Warnungen (W-*). Nutzt dieselbe Extension-Registry
#                          wie das Gate, ext: Lektionen werden also validiert
#                          statt abgewiesen. Warnungen brechen den Lauf nicht ab.
#     make export          Ein Set fuer KI-Review exportieren (ARGS="<slug>
#                          [--split-size N] ..."). Reines Python-Skript, kein
#                          Node/Engine noetig.
#
# Du brauchst Node.js (>= 20) und npm. Kein package.json nötig: die Engine
# wird mit --no-save an der in schema/engine-version.txt gepinnten Version
# installiert, exakt wie in der CI. Kein "make" auf deinem System? Dann
# führe die Befehle aus dem lint-Ziel von Hand aus, oder committe und
# lass die CI prüfen - sie prüft dasselbe.

ENGINE_PIN := $(shell cat schema/engine-version.txt)
ENGINE_STAMP := node_modules/.engine-$(ENGINE_PIN)

.PHONY: lint lint-warnings export export-anki help prose-check

help:
	@echo "make lint            - Engine-Gate lokal (Selbsttest + alle Lektionen/Manifeste)"
	@echo "make lint-warnings   - derselbe Lauf, zusätzlich mit Warnungen (W-*)"
	@echo "make prose-check      - Em-Dash, unsichtbare Zeichen, fehlende Umlaute in allen Dateien"
	@echo "make export          - Set für KI-Review exportieren (ARGS=\"<slug> [--split-size N] ...\")"
	@echo "make export-anki     - Set als Anki-Deck (.apkg) exportieren (ARGS=\"<slug> [--lang xx] [--out PATH]\")"

# Die gepinnte Engine. Wird nur installiert, wenn der Versions-Stempel fehlt
# (idempotent; ein neuer Pin in schema/engine-version.txt erzwingt eine
# Neuinstallation, weil sich der Stempel-Name ändert).
$(ENGINE_STAMP):
	@echo ">> Installiere learn-content-engine@$(ENGINE_PIN) (einmalig, lokal in node_modules/) ..."
	npm install --no-save --no-package-lock --no-audit --no-fund "learn-content-engine@$(ENGINE_PIN)" "yaml@^2.9.0"
	@touch "$(ENGINE_STAMP)"

lint: $(ENGINE_STAMP)
	node scripts/validate_with_engine.mjs --self-test
	node scripts/validate_with_engine.mjs .

# Prosa-Gate: Em-Dash, unsichtbare Zeichen und deutsche Wörter ohne ihre
# Umlaute (ae/oe/ue/ss statt ä/ö/ü/ß) in allen getrackten Dateien.
# Der Selbsttest läuft zuerst - ein Gate, das auf bekannt schlechte Eingabe
# nicht anschlägt, ist kein Gate. Braucht nur Python 3 (keine Engine, kein
# venv).
prose-check:
	@python3 scripts/check_prose.py --self-test
	@python3 scripts/check_prose.py

lint-warnings: $(ENGINE_STAMP)
	node scripts/validate_with_engine.mjs --warnings .

stable-ids: $(ENGINE_STAMP) ## Stabilitäts- und Abdeckungs-Gate (beide mitgeliefert)
	npx --no-install learn-content-engine check-stable-ids --base origin/main
	npx --no-install learn-content-engine check-stable-id-coverage

# Ein Set für KI-Review exportieren, z. B.:
#     make export ARGS="<set-slug>"
#     make export ARGS="<set-slug> --split-size 5"
# Braucht nur Python 3 + PyYAML (kein Node, keine gepinnte Engine).
export:
	@python3 scripts/export_set.py $(ARGS)

# Ein Set als Anki-Deck (.apkg) exportieren, z. B.:
#     make export-anki ARGS="<set-slug>"
#     make export-anki ARGS="<set-slug> --lang en --out /tmp/deck.apkg"
export-anki:
	@python3 scripts/export_anki.py $(ARGS)
