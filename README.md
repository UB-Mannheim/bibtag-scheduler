# bibtag-scheduler

![Python version](https://img.shields.io/badge/python-3.10-blue.svg)
![License](https://img.shields.io/github/license/UB-Mannheim/bibtag-scheduler.svg)

Erzeugt eine Pentabarf XML Datei aus dem online Programm der BiblioCon 2023,
so dass Open Source Apps wie Giggity zur Anzeige des Programms auf mobilen
Geräten genutzt werden können, z.B.

<img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-by-rooms.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-presentation.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-suche.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-programm.jpg" width="200"/> 


## Nutzung als mobile Version des Programms mit Giggity

1. Auf Android-Gerät die App [Giggity](https://github.com/Wilm0r/giggity) installieren
2. In der Liste der Veranstaltungen `BiblioCon 2023` auswählen.

### Aktualisierungen

Beim erneuten Start von Giggity kann man in der Auswahlliste bei kommenden Veranstaltungen
den Eintrag `BiblioCon 2023` lange gedrückt halten um dann in dem erscheinenden Kontext-Menu
auf `Aktualisieren` zu drücken.

Wegen kurzfristige Programmänderungen sollte man lieber nochmals das [offizielle Programm](https://dbt2023.abstractserver.com/program/)
konsultieren. Aktuell ist noch nicht klar, ob und wie häufig die Daten hier aktualisiert werden
können.


## Download der generierten XML-Datei

Die aktuell erzeuge Pentabarf-XML-Datei kann auch direkt heruntergeladen werden unter:
```
https://cloud.bib.uni-mannheim.de/s/3NdTDTKfDmz9pqy/download/bibliocon23.xml
```


## Generierung der XML-Datei

Die Generierung der XML-Datei passiert in zwei Schritten.
Zuerst werden vom Web die Daten der Veranstaltung heruntergeladen und als JSON-Dateien im `cache` Ordner gespeichert.
Daraus wird im zweiten Schritt das Programm als XML-Datei erzeugt.
Der erste Schritt muss nur erneut ausgeführt werden, wenn es Programmänderungen gab.

### Schritt 1: Dateien in den Cache herunterladen

```
cd cache
python download-data.py
```


### Schritt 2: Erzeugung der Pentabarf-XML Datei

```
python schedule.py
```


## Frühere Veranstaltungen

Der Code für den Bibliothekskongress 2022 entspricht den Stand
[0f7d0512f4e23d2db70c7406e82e2fa16b9e1f5f](https://github.com/UB-Mannheim/bibtag-scheduler/tree/0f7d0512f4e23d2db70c7406e82e2fa16b9e1f5f)
und der Code für den Bibliothekartag 2020 entspricht dem Commit
[e3f778172ece3b991a5f15e8c37ffd17df05b6c1](https://github.com/UB-Mannheim/bibtag-scheduler/tree/e3f778172ece3b991a5f15e8c37ffd17df05b6c1).
Darauf aufbauend wurde der Code hier angepasst für die BiblioCon 2023.
