# bibtag-scheduler

![Python version](https://img.shields.io/badge/python-3.7-blue.svg)
![License](https://img.shields.io/github/license/UB-Mannheim/bibtag-scheduler.svg)

Erzeugt eine Pentabarf XML Datei aus dem online Programm des Bibliothekskongresses 2022,
so dass Open Source Apps wie Giggity zur Anzeige des Programms auf mobilen
Geräten genutzt werden können, z.B.

<img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-by-rooms.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-presentation.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-suche.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-programm.jpg" width="200"/> 


## Nutzung als mobile Version des Programms mit Giggity

1. Auf Android-Gerät die App [Giggity](https://github.com/Wilm0r/giggity) installieren
2. In der Liste der Veranstaltungen `Bibliothekskongress 2022` auswählen.

### Aktualisierungen

Beim erneuten Start von Giggity kann man in der Auswahlliste bei kommenden Veranstaltungen
den Eintrag `Bibliothekskongress 2022` lange gedrückt halten um dann in dem erscheinenden Kontext-Menu
auf `Aktualisieren` zu drücken.

Wegen kurzfristige Programmänderungen sollte man lieber nochmals das [offizielle Programm](https://bid2022.abstractserver.com/program/)
konsultieren. Aktuell ist noch nicht klar, ob und wie häufig die Daten hier aktualisiert werden
können.


## Download der generierten XML-Datei

Die aktuell erzeuge Pentabarf-XML-Datei kann auch direkt heruntergeladen werden unter:
```
https://cloud.bib.uni-mannheim.de/s/QNzesdFeDg6tJ5j/download/bibtag22.xml
```


## Generierung der XML-Datei

Die Generierung der XML-Datei passiert in zwei Schritten.
Zuerst werden vom Web die Daten der Veranstaltung heruntergeladen und als JSON-Dateien im `cache` Ordner gespeichert.
Daraus wird im zweiten Schritt das Programm als XML-Datei erzeugt.
Der erste Schritt muss nur erneut ausgeführt werden, wenn es Programmänderungen gab.

### Schritt 1: Dateien in den Cache herunterladen

Für die Twitter-Daten benötigt man zuerst entsprechende [Credentials](https://developer.twitter.com/en/apps)
und muss diese in einer Datei `cache/twittercredentials.json` als JSON speichern.
Die restlichen Sachen können aber auch ohne den Teil für Twitter durchlaufen und
daher ist sind diese Credentials optional.

```
cd cache
python download-data.py
```


### Schritt 2: Erzeugung der Pentabarf-XML Datei

```
python schedule.py
```


## Frühere Veranstaltungen

Für den Bibliothekartag 2020 findet man den Code im entsprechenden Branch
[bibtag2020](https://github.com/UB-Mannheim/bibtag-scheduler/tree/bibtag2020).
Darauf aufbauend wurde der Code hier angepasst für den Bibliothekskongress 2022.
