# Faktencheck-Extrakt: Set „Psychologie der Beeinflussung"

Set: `sets/de/psych-beeinflussung` (8 Lektionen, `domain: psychology`, Deutsch).
Zweck dieser Datei: alle prüfbaren fachlichen Behauptungen und Studienzitate aus dem
Set isoliert und lesbar bereitstellen, damit eine **zweite, unabhängige KI** sie
gegenprüfen kann — ohne sich durch JSON/Schema arbeiten zu müssen.

> **Diese Datei extrahiert nur, sie bewertet nicht.** Die Aussagen sind treu aus dem
> Set übernommen (Theorie-Schritte, Card-Rückseiten/Notizen, Aufgaben). Ob sie sachlich
> korrekt sind, entscheidet die Prüfung.

---

## Prüfauftrag an die zweite KI

Prüfe jede der unten gelisteten Angaben **einzeln** und markiere sie als
**korrekt / falsch / fragwürdig**:

1. **Studienangaben:** Stimmen Autor(en), Jahr und das beschriebene Ergebnis? Ist die
   Studie der Aussage, die sie im Set belegen soll, korrekt zugeordnet?
2. **Fachliche Aussagen:** Ist die Beschreibung des Effekts/Mechanismus sachlich richtig?
3. **Zahlen / Effektstärken:** Sind genannte Zahlen korrekt wiedergegeben?
4. **Einordnung / Augenmaß:** Sind Relativierungen (z. B. „robust", „umstritten",
   „moderat", „Replikationskrise") fachlich angemessen — weder übertrieben noch falsch
   verharmlosend?

Achte besonders auf: falsche Jahreszahlen, vertauschte Autoren, falsch zugeordnete
Ergebnisse, übertriebene Effektbehauptungen, und Studien, die es so nicht gibt.
Jede gefundene Korrektur bitte mit dem **Quellenverweis** (Lektion/Element) zurückmelden,
der bei jedem Punkt angegeben ist.

---

## Lektion 1 — Priming
Quelle: `lessons/01-priming.json`

### Fachliche Kernaussagen
- Priming (Bahnung): ein vorgeschalteter Reiz aktiviert unbewusst Assoziationen und macht passende Inhalte danach leichter verfügbar. *(step `intro`, card `card-priming`)*
- **Semantisches Priming** (bedeutungsverwandte Wörter, z. B. *Arzt* nach *Krankenschwester*) gilt als **robust** und vielfach repliziert. *(step `intro`, card `card-semantisches-priming`)*
- **Perzeptuelles Priming** (leichteres Wiedererkennen eines zuvor wahrgenommenen Reizes, auch ohne bewusste Erinnerung) gilt ebenfalls als gut abgesichert. *(card `card-perzeptuelles-priming`)*
- **Social/Behavioral Priming** (beiläufige Reize verändern direkt komplexes Verhalten) gilt als **umstritten**; viele dieser Studien ließen sich nicht reproduzieren. *(step `intro`, cards `card-social-priming`, `card-priming-grenze`)*
- Gesamteinordnung: semantisches/perzeptuelles Priming robust; behaviorales Priming „klein, fragil und nicht garantiert — kein allmächtiger Steuerungsmechanismus". *(card `card-priming-grenze`)*

### Genannte Studien
- **Meyer & Schvaneveldt (1971)** — semantisches Priming, klassisch gezeigt in Lexical-Decision-Aufgaben. Belegt im Set die Robustheit des semantischen Primings. *(step `intro`, card `card-semantisches-priming`)*
- **Bargh, Chen & Burrows (1996)** — berichteten, dass Versuchspersonen nach *Alters*-Wörtern langsamer gingen. *(step `intro`, card `card-bargh-doyen`)*
- **Doyen et al. (2012)** — konnten den Bargh-Effekt unter kontrollierten Bedingungen **nicht** sauber bestätigen/replizieren. Im Set als Beispiel dafür, warum behaviorales Priming kritisch gesehen wird. *(step `intro`, card `card-bargh-doyen`)*

### Zahlen / Effektstärken
- Keine konkreten Zahlen/Effektstärken genannt (qualitative Einordnung „robust" vs. „klein/fragil").

### Einordnungs-/Augenmaß-Aussagen
- **Replikationskrise:** seit den **frühen 2010er-Jahren** ließen sich viele klassische Studien nicht reproduzieren, besonders behaviorales Priming. Beginn um **2011** (erste Zweifel am social Priming, Betrugsfall Stapel), breit rezipierter Wendepunkt der **Open-Science-Replikationsreport 2015** (Open Science Collaboration); Folge: vorsichtigere Prüfung mit Präregistrierung. *(step `intro`, card `card-replikationskrise`)*
- „Priming ist real, aber kein allmächtiger Hebel." *(step `intro`)*
- Hinweis im Set: „Beide Studien [Bargh; Doyen] sind real und korrekt zugeordnet." *(card `card-bargh-doyen`)*

---

## Lektion 2 — Framing-Effekt
Quelle: `lessons/02-framing.json`

### Fachliche Kernaussagen
- Framing-Effekt: dieselbe Information wird je nach Formulierung („Verpackung") unterschiedlich bewertet und kann zu anderen Entscheidungen führen; der sachliche Inhalt bleibt gleich. *(step `intro`, card `card-framing`)*
- **Gewinn- vs. Verlust-Framing:** im Gewinn-Frame (z. B. *90 % überleben*) wählen Menschen eher risikoscheu, im Verlust-Frame (*10 % sterben*) eher risikofreudig. *(card `card-gewinn-verlust`)*
- Mechanismus dahinter: **Verlustaversion** — Verluste wiegen subjektiv schwerer als gleich große Gewinne. *(step `intro`, card `card-gewinn-verlust`)*
- **Attribut-Framing:** ein Merkmal positiv/negativ beschrieben (*95 % fettfrei* statt *5 % Fett*) wird unterschiedlich bewertet. *(step `intro`, card `card-attribut-framing`)*
- Abgrenzung: Framing = Art der Formulierung einer Information; Priming = vorgeschaltete Reize, die unabhängig vom Inhalt Denkmuster bahnen. *(card `card-framing-priming`)*

### Genannte Studien
- **Tversky & Kahneman (1981)** — klassisches Framing-Experiment, das *Asian disease problem*: identische Überlebenszahlen führten je nach Gewinn-/Verlust-Formulierung zu gegensätzlichen Entscheidungen. Im Set als „reale, vielfach replizierte Studie" bezeichnet. Die Forscher werden im Set auch mit der Prospect Theory verknüpft. *(step `intro`, card `card-asian-disease`, exercise `ex-select-studie`)*

### Zahlen / Effektstärken
- *95 % fettfrei* vs. *5 % Fett* (Attribut-Framing-Beispiel). *(step `intro`)*
- *90 % überleben* vs. *10 % sterben* (Gewinn-/Verlust-Beispiel). *(card `card-gewinn-verlust`)*
- Asian disease: *200 von 600 werden gerettet* (Gewinn) vs. *400 von 600 sterben* (Verlust), als mathematisch identisch dargestellt. *(step `intro`)*

### Einordnungs-/Augenmaß-Aussagen
- „Framing ist real und vielfach repliziert — aber **ein Einfluss, keine Determinante**." Vorwissen, Motivation, klare Zahlen, Nachdenken können den Effekt abschwächen. *(step `intro`, card `card-framing-grenze`)*

---

## Lektion 3 — Ankereffekt
Quelle: `lessons/03-ankereffekt.json`

### Fachliche Kernaussagen
- Ankereffekt: eine zuerst genannte Information (oft eine Zahl) dient als Bezugspunkt und zieht Folgeurteile in ihre Richtung; wirkt selbst dann, wenn der Anker offensichtlich zufällig/irrelevant ist. *(step `intro`, card `card-anker`)*
- **Zwei Erklärungsmodelle nebeneinander (als Entwicklung der Theorie dargestellt):**
  - *Ursprüngliches Modell — Anchoring and Adjustment (Tversky & Kahneman, 1974):* Menschen passen ihr Urteil vom Anker ausgehend an, hören aber meist zu früh auf, sodass das Ergebnis nahe am Anker bleibt („zu früh aufhören beim Anpassen"). *(step `intro`, card `card-anpassung`)*
  - *Moderne Verfeinerung — Selective Accessibility / selektive Verfügbarkeit (Strack & Mussweiler, 1997):* besonders bei zufälligen, extern vorgegebenen Ankern (wie dem Glücksrad) aktiviert der Anker selektiv passende Informationen im Gedächtnis, die danach leichter verfügbar sind und das Urteil in Richtung Anker verschieben („das Gehirn sucht selektiv nach Infos, die zum Anker passen"). *(step `intro`, card `card-selektive-verfuegbarkeit`)*
- **Anwendung Verhandlung:** das erste Angebot setzt einen Bezugspunkt; wer zuerst nennt, prägt oft den Rahmen. *(card `card-anker-verhandlung`)*
- Abgrenzung: Anker = zuerst genannter Bezugswert prägt die Schätzung; Framing = positive/negative Formulierung prägt die Bewertung. *(card `card-anker-abgrenzung`)*

### Genannte Studien
- **Tversky & Kahneman (1974)** — Glücksrad-Experiment: ein per Glücksrad erzeugter Zufallswert beeinflusste die anschließende Schätzung des Anteils afrikanischer Länder in der UNO; höherer Anker → höhere Schätzung, niedriger Anker → niedrigere. Im Set: „reale Studie", zeigt, dass selbst offensichtlich zufällige Anker wirken. Im Set dem ursprünglichen Anchoring-and-Adjustment-Modell zugeordnet. *(step `intro`, card `card-tk-1974`, card `card-anpassung`, exercise `ex-select-anker-studie`)*
- **Strack & Mussweiler (1997)** — dem Selective-Accessibility-Modell zugeordnet: der Anker aktiviert selektiv bestätigende Informationen im Gedächtnis, wodurch sich das Urteil Richtung Anker verschiebt. Im Set als moderne Verfeinerung neben (nicht statt) Anchoring and Adjustment dargestellt. *(step `intro`, card `card-selektive-verfuegbarkeit`)*

### Zahlen / Effektstärken
- Keine konkreten Zahlen/Effektstärken genannt (Beschreibung qualitativ).

### Einordnungs-/Augenmaß-Aussagen
- „Der Ankereffekt ist robust und vielfach repliziert", aber **begrenzbar**: bewusstes Hinterfragen, Gegenargumente oder Fachwissen reduzieren den Einfluss. „Robust heißt nicht unausweichlich." *(step `intro`, card `card-anker-grenze`)*

---

## Lektion 4 — Kognitive Dissonanz
Quelle: `lessons/04-kognitive-dissonanz.json`

### Fachliche Kernaussagen
- Kognitive Dissonanz: unangenehmer Spannungszustand, wenn Überzeugungen/Werte und Verhalten nicht zusammenpassen (Beispiel: rauchen trotz Wissens um die Schädlichkeit). *(step `intro`, card `card-dissonanz`)*
- **Dissonanzreduktion:** Druck, die Spannung zu verringern — Einstellung ändern, Verhalten anpassen oder neue Rechtfertigungen suchen; oft ist die Einstellung leichter zu ändern als bereits gezeigtes Verhalten. *(step `intro`, card `card-reduktion`)*
- **Unzureichende Rechtfertigung:** fehlt ein starker äußerer Grund, ändert man eher die innere Einstellung, um das Verhalten stimmig erscheinen zu lassen. *(step `intro`, card `card-rechtfertigung`)*
- **Als Hebel der Beeinflussung:** wer jemanden zu einer kleinen freiwilligen Handlung bewegt, kann eine Einstellungsänderung anstoßen (Verbindung zu Foot-in-the-door: „aus Handlung folgt Haltung"). *(card `card-dissonanz-beeinflussung`)*

### Genannte Studien
- **Leon Festinger (1957)** — Begründer der Theorie der kognitiven Dissonanz. *(step `intro`, card `card-dissonanz`)*
- **Festinger & Carlsmith (1959)** — 1-Dollar/20-Dollar-Experiment: Versuchspersonen erledigten eine langweilige Aufgabe und behaupteten danach gegenüber einer anderen Person, sie sei interessant gewesen; wer nur **1 Dollar** erhielt, fand die Aufgabe hinterher tatsächlich interessanter als wer **20 Dollar** erhielt. Erklärung: geringe Belohnung = unzureichende äußere Rechtfertigung → Einstellung passt sich an. Im Set: „reale, klassische Studie". *(step `intro`, card `card-festinger-carlsmith`, exercise `ex-select-studie`)*

### Zahlen / Effektstärken
- **1 Dollar** vs. **20 Dollar** Belohnung (zentrale Bedingung des Experiments). *(step `intro`, card `card-festinger-carlsmith`)*

### Einordnungs-/Augenmaß-Aussagen
- „Dissonanz wird *nicht immer* durch Einstellungsänderung aufgelöst." Alternativen: Spannung aushalten, störende Information abwerten oder Verhalten ändern. „Die Richtung der Auflösung ist nicht festgelegt." *(step `intro`, card `card-dissonanz-grenze`)*

---

## Lektion 5 — Reziprozität
Quelle: `lessons/05-reziprozitaet.json`

### Fachliche Kernaussagen
- Reziprozitätsprinzip: wer etwas erhält (Geschenk, Gefallen, Zugeständnis), verspürt sozialen Druck, sich zu revanchieren. Eines der sechs Einflussprinzipien nach **Robert Cialdini**. *(step `intro`, card `card-reziprozitaet`)*
- **Door-in-the-face:** reziproke Zugeständnis-Technik — auf eine bewusst überzogene erste Bitte folgt eine kleinere; das sichtbare Nachgeben erzeugt Druck, ebenfalls nachzugeben. *(step `intro`, card `card-door-in-the-face`)*

### Genannte Studien
- **Norm der Reziprozität — Alvin Gouldner (1960):** weit verbreitete soziale Norm „man soll denen helfen, die einem geholfen haben"; von Gouldner als nahezu universelle soziale Erwartung beschrieben. *(step `intro`, card `card-gouldner`)*
- **Regan (1971):** Cola-und-Lose-Experiment — ein vermeintlicher Mitproband spendierte unaufgefordert eine Cola; Versuchspersonen, die die Cola erhalten hatten, kauften ihm danach im Schnitt mehr Lose ab. Im Set: „reale Studie", zeigt die Reziprozitätswirkung eines kleinen Gefallens. *(step `intro`, card `card-regan`, exercise `ex-select-regan`)*
- **Cialdini et al. (1975):** der Door-in-the-face-Technik zugeordnet (beruht auf reziproken Zugeständnissen, nicht auf einem Geschenk). *(step `intro`, card `card-door-in-the-face`)*

### Zahlen / Effektstärken
- Keine konkreten Zahlen („im Schnitt mehr Lose", qualitativ). *(step `intro`)*

### Einordnungs-/Augenmaß-Aussagen
- „Reziprozität ist eine **empirisch belegte Tendenz, kein Automatismus**." Wer ein Geschenk als Manipulationsversuch durchschaut, fühlt sich oft nicht verpflichtet. „Eine Wahrscheinlichkeit, keinen Schalter." *(step `intro`, card `card-reziprozitaet-grenze`)*

---

## Lektion 6 — Soziale Bewährtheit (social proof)
Quelle: `lessons/06-soziale-bewaehrtheit.json`

### Fachliche Kernaussagen
- Soziale Bewährtheit (*social proof*): bei Unsicherheit/Mehrdeutigkeit orientieren sich Menschen am Verhalten anderer, um zu entscheiden, was richtig ist. Eines der Einflussprinzipien nach **Cialdini**. *(step `intro`, card `card-soziale-bewaehrtheit`)*
- **Informationaler sozialer Einfluss:** das Verhalten anderer wird als Information über die Wirklichkeit genutzt; abgegrenzt vom **normativen** Einfluss (Dazugehören-Wollen). *(step `intro`, cards `card-informationaler-einfluss`)*
- **Verstärker:** der Effekt wirkt stärker bei Unsicherheit und wenn die anderen einem ähnlich sind. *(step `intro`, card `card-unsicherheit-aehnlichkeit`)*

### Genannte Studien
- **Deutsch & Gerard (1955):** dem informationalen (vs. normativen) sozialen Einfluss zugeordnet. *(step `intro`, card `card-informationaler-einfluss`)*
- **Goldstein, Cialdini & Griskevicius (2008):** Feldexperiment in Hotels — Hinweisschilder, dass die meisten Gäste ihre Handtücher wiederverwenden, steigerten die Wiederverwendung stärker als ein reiner Umwelt-Appell. Im Set: „reales Feldexperiment", Effekt „messbar, aber moderat". *(step `intro`, card `card-hotel-handtuch`)*

### Zahlen / Effektstärken
- Keine konkreten Zahlen; Effekt qualitativ als „messbar, aber moderat" beschrieben. *(step `intro`, card `card-hotel-handtuch`)*

### Einordnungs-/Augenmaß-Aussagen
- „Das Verhalten der Mehrheit ist nicht automatisch richtig." Wer klare eigene Information oder Fachwissen hat, folgt der Masse seltener. „Eine Orientierungshilfe, kein Wahrheitsbeweis." *(step `intro`, card `card-bewaehrtheit-grenze`)*

---

## Lektion 7 — Foot-in-the-door
Quelle: `lessons/07-foot-in-the-door.json`

### Fachliche Kernaussagen
- Foot-in-the-door: wer zuerst einer kleinen Bitte zustimmt, willigt anschließend mit höherer Wahrscheinlichkeit auch in eine größere Bitte ein. *(step `intro`, card `card-fitd`)*
- **Erklärung Selbstwahrnehmung:** nach der ersten Zusage sieht man sich als hilfsbereite/engagierte Person und handelt konsistent weiter; anknüpfend an die Selbstwahrnehmungstheorie (**Bem, 1972**) und das Konsistenzstreben. *(step `intro`, card `card-selbstwahrnehmung`)*
- **Abgrenzung zu Door-in-the-face:** Foot-in-the-door beginnt klein und steigert (Mechanismus Konsistenz); Door-in-the-face beginnt überzogen und reduziert (Mechanismus Reziprozität). *(step `intro`, card `card-fitd-vs-ditf`)*

### Genannte Studien
- **Freedman & Fraser (1966):** klassisches Experiment — Hausbesitzer, die zuerst einer kleinen Bitte zustimmten (z. B. kleinen Aufkleber anbringen / kurze Petition unterschreiben), willigten danach deutlich häufiger ein, ein großes Verkehrssicherheits-Schild im Vorgarten aufzustellen. Im Set: „reale, klassische Studie". *(step `intro`, card `card-freedman-fraser`, exercise `ex-select-fitd-studie`)*
- **Bem (1972)** — als Urheber der Selbstwahrnehmungstheorie genannt (Standardreferenz *Advances in Experimental Social Psychology*). *(card `card-selbstwahrnehmung`)*

### Zahlen / Effektstärken
- Keine konkreten Zahlen („deutlich häufiger", qualitativ). *(step `intro`)*

### Einordnungs-/Augenmaß-Aussagen
- „Der Effekt ist real, aber **moderat und nicht garantiert**." Hängt von Kontext, Größe der Bitten und Freiwilligkeit der ersten Zusage ab. „Eine belegte Tendenz — kein sicherer Hebel." *(step `intro`, card `card-fitd-grenze`)*

---

## Lektion 8 — Wiederholung & Synthese
Quelle: `lessons/08-wiederholung-beeinflussung.json`

### Zusammenfassende Kernaussagen (Wiederholung der obigen Effekte)
- **Priming:** vorgeschalteter Reiz aktiviert Assoziationen; robust nur als semantisches/perzeptuelles Priming; behaviorales Priming umstritten (Replikationskrise). *(card `card-s-priming`, exercise `ex-select-priming-robust`)*
- **Framing:** gleiche Information, andere Verpackung → andere Bewertung; „ein Einfluss, keine Determinante" — zugeordnet **Tversky & Kahneman (1981)**. *(card `card-s-framing`)*
- **Ankereffekt:** eine zuerst genannte Zahl prägt Folgeurteile — zugeordnet **Tversky & Kahneman (1974)**. *(card `card-s-anker`)*
- **Kognitive Dissonanz:** Spannung zwischen Haltung und Handlung — zugeordnet **Festinger (1957)** und **Festinger & Carlsmith (1959)**. *(card `card-s-dissonanz`)*
- **Reziprozität:** wer etwas erhält, fühlt sich verpflichtet zu revanchieren — **Cialdini**; Norm der Reziprozität **(Gouldner, 1960)**. *(card `card-s-reziprozitaet`)*
- **Soziale Bewährtheit:** Verhalten anderer als Orientierung, besonders bei Unsicherheit — **Cialdini**; informationaler sozialer Einfluss. *(card `card-s-bewaehrtheit`)*
- **Foot-in-the-door:** kleine Zusage erhöht Bereitschaft zur großen Bitte — **Freedman & Fraser (1966)**. *(card `card-s-fitd`)*

### Einordnungs-/Augenmaß-Aussagen
- Roter Faden des Sets: „Alle diese Effekte sind **empirisch belegte Tendenzen**, keine garantierten Hebel" — sie beschreiben, was im Schnitt wahrscheinlicher wird, nicht was sicher passiert. Effektstärken nicht aufblasen, Studien korrekt zuordnen. *(step `intro`, card `card-s-augenmass`)*

---

## Gesamtliste der genannten Studien (zur schnellen Querprüfung)

| # | Studie / Quelle | Jahr | Im Set zugeordnet zu | Quelle (Lektion) |
|---|---|---|---|---|
| 1 | Meyer & Schvaneveldt | 1971 | semantisches Priming (Lexical-Decision) | L1 |
| 2 | Bargh, Chen & Burrows | 1996 | behaviorales Priming (langsameres Gehen nach Alters-Wörtern) | L1 |
| 3 | Doyen et al. | 2012 | Nicht-Replikation des Bargh-Effekts | L1 |
| 4 | Tversky & Kahneman | 1981 | Framing / Asian disease problem | L2, L8 |
| 5 | Tversky & Kahneman | 1974 | Ankereffekt / Glücksrad-Experiment; ursprüngliches Anchoring-and-Adjustment-Modell | L3, L8 |
| 6 | Festinger | 1957 | Theorie der kognitiven Dissonanz | L4, L8 |
| 7 | Festinger & Carlsmith | 1959 | 1-Dollar/20-Dollar-Experiment | L4, L8 |
| 8 | Gouldner | 1960 | Norm der Reziprozität | L5, L8 |
| 9 | Regan | 1971 | Cola-und-Lose-Experiment (Reziprozität) | L5 |
| 10 | Cialdini et al. | 1975 | Door-in-the-face | L5 |
| 11 | Deutsch & Gerard | 1955 | informationaler vs. normativer sozialer Einfluss | L6 |
| 12 | Goldstein, Cialdini & Griskevicius | 2008 | Hotel-Handtuch-Feldexperiment (social proof) | L6 |
| 13 | Freedman & Fraser | 1966 | Foot-in-the-door | L7, L8 |
| 14 | Bem (Selbstwahrnehmungstheorie) | 1972 | Erklärung von Foot-in-the-door | L7 |
| 15 | Strack & Mussweiler | 1997 | Ankereffekt / Selective-Accessibility-Modell (card `card-selektive-verfuegbarkeit`) | L3 |
| – | Robert Cialdini | — | Sammlung der sechs Einflussprinzipien | L5, L6 |
