# bibtag-scheduler

![Python version](https://img.shields.io/badge/python-3.7-blue.svg)

Erzeugt eine Pentabarf XML Datei aus dem Programm des Bibliothekartags 2020,
so dass Open Source Apps wie Giggity zur Anzeige des Programms auf mobilen
Geräten genutzt werden können, z.B.

<img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-by-rooms.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-presentation.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-suche.jpg" width="200"/> <img src="https://rawgit.com/UB-Mannheim/ubma-screenshots/master/bibtag-scheduler/giggity-programm.jpg" width="200"/> 

## Nutzung als mobile Version des Programms

### Mit Giggity

1. Auf Android-Gerät die App [Giggity](https://github.com/Wilm0r/giggity) installieren
2. Neue Veranstaltung über das `+` hinzufügen
3. Aktuell erzeugte Datei `https://cloud.bib.uni-mannheim.de/index.php/s/AwMc2ao8C2fX8rJ/download` eingeben

### Aktualisierungen

Wegen kurzfristige Programmänderungen sollte man lieber nochmals das [offizielle Programm](https://bibliothekartag2020.de/programm/)
konsultieren. Aktuell ist noch nicht klar, ob und wie häufig die Daten hier aktualisiert werden
können.

Beim erneuten Start von Giggity kann man in der Auswahlliste bei kommenden Veranstaltungen
den Eintrag Bibliothekartag 2020 lange gedrückt halten um dann in dem erscheinenden Kontext-Menu
auf Aktualisieren zu drücken.


## Generierung der Datei

### Dateien in den Cache herunterladen

Prinzipiell kann man hier das Skript
```
./cache/download-data.sh
```
nutzen um die Daten lokal herunterzuladen. Dabei muss man aber die auskommentierten
Zeilen ggf. anpassen. Zudem werden nur die Daten der bekannten Sessions und
Präsentationen angefragt. Bei größeren Programmänderungen müssten diese for-Loops
angepasst werden.

### Erzeugung der Pentabarf-XML Datei

```
python schedule.py
```
