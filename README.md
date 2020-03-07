# bibtag-scheduler

![Python version](https://img.shields.io/badge/python-3.7-blue.svg)
![License](https://img.shields.io/github/license/UB-Mannheim/bibtag-scheduler.svg)

Erzeugt eine Pentabarf XML Datei aus dem Programm des Bibliothekartags 2020,
so dass Open Source Apps wie Giggity zur Anzeige des Programms auf mobilen
Geräten genutzt werden können, z.B.

<img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-by-rooms.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-presentation.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-suche.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-programm.jpg" width="200"/> 

## Nutzung als mobile Version des Programms

### Mit Giggity

1. Auf Android-Gerät die App [Giggity](https://github.com/Wilm0r/giggity) installieren
2. In der Liste der Veranstaltungen `Bibliothekartag 2020` auswählen.


### Aktualisierungen

Wegen kurzfristige Programmänderungen sollte man lieber nochmals das [offizielle Programm](https://bibliothekartag2020.de/programm/)
konsultieren. Aktuell ist noch nicht klar, ob und wie häufig die Daten hier aktualisiert werden
können.

Beim erneuten Start von Giggity kann man in der Auswahlliste bei kommenden Veranstaltungen
den Eintrag Bibliothekartag 2020 lange gedrückt halten um dann in dem erscheinenden Kontext-Menu
auf Aktualisieren zu drücken.


### Download der XML-Datei

Die aktuell erzeuge Pentabarf-XML-Datei kann auch direkt heruntergeladen werden unter:
```
https://cloud.bib.uni-mannheim.de/index.php/s/AwMc2ao8C2fX8rJ/download
```


## Generierung der XML-Datei

Zuerst muss einmalig man die JSON-Daten herunterladen und als Dateien im `cache` Ordner speichern.
Daraus kann das Programm als XML-Datei erzeugt werden.
Der erste Schritt muss nur erneut ausgeführt werden, wenn es Programmänderungen gab.

### Dateien in den Cache herunterladen

```
cd cache
python download-data.py
```

Für die Twitter-Daten benötigt man zuerst entsprechende [Credentials](https://developer.twitter.com/en/apps)
und muss diese in einer Datei `cache/twittercredentials.json` als JSON speichern

### Erzeugung der Pentabarf-XML Datei

```
python schedule.py
```
