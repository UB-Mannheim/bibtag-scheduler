# bibtag-scheduler

![Python version](https://img.shields.io/badge/python-3.10-blue.svg)
![License](https://img.shields.io/github/license/UB-Mannheim/bibtag-scheduler.svg)

Erzeugt eine Pentabarf XML Datei aus dem online Programm der BiblioCon,
so dass Open Source Apps wie Giggity zur Anzeige des Programms auf mobilen
Geräten genutzt werden können, z.B.

<img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-by-rooms.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-presentation.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-suche.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-programm.jpg" width="200"/> 


## Nutzung als mobile Version des Programms mit Giggity

1. Auf Android-Gerät die App [Giggity](https://github.com/Wilm0r/giggity) installieren
2. In der Liste der Veranstaltungen den aktuellen `BiblioCon`-Eintrag auswählen.

### Aktualisierungen

Beim erneuten Start von Giggity kann man in der Auswahlliste bei kommenden Veranstaltungen
den `BiblioCon`-Eintrag lange gedrückt halten um dann in dem erscheinenden Kontext-Menu
auf `Aktualisieren` zu drücken.

Wegen kurzfristige Programmänderungen sollte man lieber nochmals das offizielle Programm
konsultieren. Bisher wurde die Daten jeweils wöchentlich vor dem Start der Konferenz
aktualisiert und dann an jedem Veranstaltungstag nochmals.


## [DEV] Generierung der XML-Datei

Die Generierung der XML-Datei passiert in zwei Schritten.
Zuerst werden vom Web die Daten der Veranstaltung heruntergeladen und als JSON-Dateien im `cache` Ordner gespeichert.
Daraus wird im zweiten Schritt das Programm als XML-Datei erzeugt.

### Schritt 1: Dateien in den Cache herunterladen

```
cd cache
python download-data.py
```


### Schritt 2: Erzeugung der Pentabarf-XML Datei

```
python schedule.py
```

## [DEV] Erzeugte Datei in Giggity einlesen

In Giggity kann man die erzeugte Pantabarf-XML-Datei direkt einlesen,
wenn man diese zuerst online verfügbar macht (z.B. über einen Cloud-Anbieter).
Wichtig ist dabei, dass man die XML-Datei direkt verlinkt und nicht nur eine
Webseite mit der Möglichkeit die Datei herunterzuladen. Diese Möglichkeit
die erzeugten Datei einfach einzulesen ist zum Testen nützlich.

Sobald man einen stabilen Link zur XML-Datei hat, kann man diesen prinzipiell
auch mit anderen teilen so dass diese auch das Programm in Giggity nutzen
können. Praktisch noch einfacher geht es aber über einen eigenen Menüeintrag,
vgl. nächster Punkt.

Konkret wird von uns eine NextCloud-Instanz genutzt und die Datei über einen öffentlichen
Link geteilt. Neue Versionen des Programmes können dann in der NextCloud hochgeladen
werden (alte Version überschreiben), wobei der Link gleichbleibt. Über den
Aktualisierungsmechanismus von Giggity werden die Aktualasierung auch für alle
anderen verteilt.

## [DEV] Giggity-Menüeintrag erstellen

Mit dem Link auf die Pentabarf-XML-Datei und einigen anderen Daten kann man
in ein entpsrechendes JSON-Datei schreiben um einen Menüeintrag in Giggity
zu kreieren. Beispielsweise kann man weitere Links angeben oder einen
Übersichtsplan einbinden. Details findet man in den [PRs der letzten Jahre](https://github.com/Wilm0r/giggity/pulls?q=is%3Apr+author%3Azuphilip).


## Historie

Der aktuelle Code ist für die aktuelle BiblioCon angepasst, aber
frühere Stände wurde auch schon für die voherigen Konferenzen genutzt:
- BiblioCon 2024: [0b90e25469ad4f69b67741d9c0e4e6ac7aad88a8](https://github.com/UB-Mannheim/bibtag-scheduler/tree/0b90e25469ad4f69b67741d9c0e4e6ac7aad88a8)
- BiblioCon 2023: [1db0c4c91ad03bd09946de444ed5ee50a47bc247](https://github.com/UB-Mannheim/bibtag-scheduler/tree/1db0c4c91ad03bd09946de444ed5ee50a47bc247)
- Bibliothekskongress 2022: [0f7d0512f4e23d2db70c7406e82e2fa16b9e1f5f](https://github.com/UB-Mannheim/bibtag-scheduler/tree/0f7d0512f4e23d2db70c7406e82e2fa16b9e1f5f)
- Bibliothekartag 2020: [e3f778172ece3b991a5f15e8c37ffd17df05b6c1](https://github.com/UB-Mannheim/bibtag-scheduler/tree/e3f778172ece3b991a5f15e8c37ffd17df05b6c1)
