#!/usr/bin/env python3

from datetime import date, datetime
from pathlib import Path
import html
import json
import re
import urllib.parse
from xml.dom import minidom

from pentabarf.Conference import Conference
from pentabarf.Day import Day
from pentabarf.Event import Event
from pentabarf.Person import Person
from pentabarf.Room import Room

conference = Conference(
    title="BiblioCon 2023",
    start=date(2023, 5, 23),
    end=date(2023, 5, 26),
    days=4,
    timeslot_duration="00:30",
    venue="Hannover Congress Centrum",
    city="Hannover"
)

with open("cache/index.json") as file:
    data = json.load(file)
    allDays = ["2023-05-23", "2023-05-24", "2023-05-25", "2023-05-26"]
    differentDays = [x['day']['date'] for x in data if x['day']['date'] not in allDays]
    if len(differentDays) > 0:
        print("ERROR: different days are found, which has to fixed before continuing", differentDays)
        exit()
    rooms = [
        "Kuppelsaal",
        "Niedersachsenhalle A (mit Streaming)",
        "Niedersachsenhalle B",
        "Eilenriedehalle B",
        "Blauer Saal",
        "Roter Saal (mit Streaming)",
        "Konferenzraum 27/28",
        "Bonatz Saal (mit Streaming)",
        "Runder Saal",
        "Future Meeting Space A",
        "Future Meeting Space B",
        "#Freiraum 23",
        "Konferenzraum 7 & 9",
        "Konferenzraum 8 & 10",
        "Konferenzraum 11 & 13",
        "Konferenzraum 12 & 14",
        "Konferenzraum 15",
        "Konferenzraum 16",
        "Konferenzraum 17",
        "Konferenzraum 18",
        "Foyers",
    ]
    differentRooms = [x['room']['name'] for x in data if x['room']['name'] not in rooms]
    if len(differentRooms) > 0:
        print("ERROR: different rooms are found, which has to fixed before continuing", differentRooms)
        exit()

    for dayText in allDays:
        time = datetime.strptime(dayText, "%Y-%m-%d").isoformat('T')#temp
        day = Day(date=datetime.strptime(dayText, "%Y-%m-%d"))
        #day = Day(date=date.fromisoformat(dayText))
        for roomName in rooms:
            correspondingSessions = [x for x in data if x['room']['name'] == roomName and x['day']['date'] == dayText]
            room = Room(name=roomName)
            for session in correspondingSessions:
                session['id'] = str(session['id'])
                abstract = None

                meeting_type = session['session_type']['name']
                if meeting_type.startswith('Themenkreis') or meeting_type.startswith('TK'):
                    meeting_type = "Vortragssession"
                #if session['type'].startswith('Hands-On Lab'):
                #    type = "Hands-On Lab"

                eventsAdded = False
                # try to add the presentations instead of the complete session
                # thus first check whether there are some additional data for this session
                if Path('cache/s' + str(session['id']) + '.json').is_file():
                    with open('cache/s' + str(session['id']) + '.json') as sessionFile:
                        sessionData = json.load(sessionFile)[0]

                        if 'presentations' in sessionData and len(sessionData['presentations']) > 0:
                            # for some sessions (e.g. the opening) there are several presentations at the same time, which looks more
                            # like an error or some unusual pattern, and therefore we better don't take the individual
                            # presentations but the whole session
                            startingTimes = [x['start_time'] for x in sessionData['presentations']]
                            if len(startingTimes) == len(list(dict.fromkeys(startingTimes))):

                                for presentationData in sessionData['presentations']:

                                    title = html.unescape(presentationData['presentation']['title'])
                                    # some titles are put into unnecessary html tags, which we want to clean away
                                    # e.g. <p data-pm-slice="1 1 []">Ground Truth-Erstellung und Modelltraining mit eScriptorium</p>
                                    title = re.sub("<[^<>]*>", "", title)
                                    # add the prefix "S" with session id to the title of the presentations
                                    if len(startingTimes) > 1:
                                        title = "S" + str(session['id']) + ": " + title

                                    start = presentationData['start_time']
                                    end = presentationData['end_time']
                                    if len(startingTimes) == 1 and start == end:
                                        start = session['start_time']
                                        end = session['end_time']
                                    hoursDiff = int(end[:2]) - int(start[:2])
                                    minutesDiff = int(end[3:5]) - int(start[3:5])
                                    if minutesDiff < 0:
                                        hoursDiff -= 1
                                        minutesDiff += 60

                                    abstract = ""
                                    if len(startingTimes) > 1:
                                        sessionUrl = "https://dbt2023.abstractserver.com/program/#/details/sessions/" + session['id']
                                        abstract = "Session: <a href='" + sessionUrl + "'>" + session['title'] + " (S" + session['id'] + ")</a><br/><br/>"
                                        #if session['content']['outline'] is not None:
                                        #    print('WARN: outline for this session is ignored', session['id'], session['content']['outline'])

                                    abstractAdded = False
                                    if Path('cache/p' + str(presentationData['presentation']['id']) + '.json').is_file():
                                        with open('cache/p' + str(presentationData['presentation']['id']) + '.json') as presentationFile:
                                            presentationFileData = json.load(presentationFile)[0]
                                            if 'abstract_enriched' in presentationFileData:
                                                abstract += presentationFileData['abstract_enriched']
                                                abstractAdded = True
                                    if not abstractAdded and len(startingTimes) == 1:
                                        if session['content']['outline'] is not None:
                                            abstract = session['content']['outline']
                                    if 'target_group' in presentationFileData['content'] and presentationFileData['content']['target_group'] is not None:
                                        abstract += "<p><strong>Zielgruppe:</strong> " + presentationFileData['content']['target_group'] + "</p>"
                                    if 'stich_schlagwort' in presentationFileData['content'] and presentationFileData['content']['stich_schlagwort'] is not None:
                                        abstract += "<p><strong>Stichworte:</strong> " + presentationFileData['content']['stich_schlagwort'] + "</p>"

                                    presentationObject = Event(
                                        id='p' + str(presentationData['presentation']['id']),
                                        date=datetime.fromisoformat(dayText + "T" + start + ":00+02:00"),
                                        start=start,
                                        duration='%02d:%02d' % (hoursDiff, minutesDiff),
                                        track=session['session_type']['name'],
                                        abstract=abstract,
                                        title=title,
                                        type='Vortrag'
                                    )

                                    # personList = []
                                    for author in presentationData['presentation']['persons']:
                                        authorName = author['person']['first_name'] + ' ' + author['person']['last_name']
                                        person = Person(name=authorName, id=author['person']['id'])
                                        presentationObject.add_person(person)

                                    room.add_event(presentationObject)

                                eventsAdded = True
                            else:
                                print("WARNING: Found several presentations at the same time in this session", session['id'], session['title'], session['session_type']['name'])
                                # create an abstract for the whole session which will be added below
                                abstract = "<ul>"
                                for presentationData in sessionData['presentations']:
                                    abstract += "<li>" + presentationData['start_time'] + "-" + presentationData['end_time'] + ": " + presentationData['presentation']['title']
                                    if 'persons' in presentationData['presentation']:
                                        for author in presentationData['presentation']['persons']:
                                            abstract += '<br/>' + author['person']['first_name'] + ' ' + author['person']['last_name']
                                    abstract += '</li>'
                                abstract += '</ul>'

                            endingTimes = [x['end_time'] for x in sessionData['presentations']]
                            if session['end_time'] not in endingTimes:
                                print("WARNING: Session goes longer than any presentation", session['id'], session['title'], dayText, session['start_time'], session['end_time'])

                # add event for the whole session when no events are yet added
                if not eventsAdded:

                    if 'content' in session and 'outline' in session['content'] and session['content']['outline'] != None:
                        if not abstract:
                            abstract = ""
                        abstract = session['content']['outline'] + abstract
                    if 'target_group' in session['content'] and session['content']['target_group'] is not None:
                        abstract += "<p><strong>Zielgruppe:</strong> " + session['content']['target_group'] + "</p>"
                    if 'stich_schlagwort' in session['content'] and session['content']['stich_schlagwort'] is not None:
                        abstract += "<p><strong>Stichworte:</strong> " + session['content']['stich_schlagwort'] + "</p>"
                    duration = (session['end_time_timestamp'] - session['start_time_timestamp'] ) // 60
                    sessionObject = Event(
                        id=session['id'],
                        date=datetime.fromisoformat(dayText + "T" + session['start_time'] + ":00+02:00"),
                        start=session['start_time'],
                        duration='%02d:%02d' % ((duration // 60), (duration % 60)),
                        track=session['session_type']['name'],
                        abstract=abstract,
                        title=html.unescape(session['title']),
                        type=meeting_type,
                    )

                    if sessionData and 'persons' in sessionData:
                        for author in sessionData['persons']:
                            person = Person(name=author['person']['first_name'] + ' ' + author['person']['last_name'], id=author['person']['id'])
                            sessionObject.add_person(person)

                    room.add_event(sessionObject)

            day.add_room(room)

        conference.add_day(day)


xmldata = conference.generate("Erzeugt von https://github.com/UB-Mannheim/bibtag-scheduler/ um " + str(datetime.now()))
reparsed = minidom.parseString(xmldata.decode("utf-8"))
# delete day_change as it cannot be empty
for node in reparsed.getElementsByTagName('day_change'):
    node.parentNode.removeChild(node)
# delete some empty nodes and empty attributes
deleted = 0
for ignore in ['description', 'conf_url', 'full_conf_url', 'released']:
    for node in reparsed.getElementsByTagName(ignore):
        if node.toxml() == "<" + ignore + "/>":
            node.parentNode.removeChild(node)
            deleted += 1
# delete all date nodes which are unneccessary and make trouble because of the timezoning
#for node in reparsed.getElementsByTagName('date'):
#    node.parentNode.removeChild(node)
#    deleted += 1
print("INFO: Deleted", deleted, "empty nodes + date nodes")
for node in reparsed.getElementsByTagName('person'):
    if node.getAttribute('id') == "None":
        node.removeAttribute('id')

# Output in file
with open("bibliocon23.xml", 'w', encoding="utf-8") as outfile:
    outfile.write(reparsed.toprettyxml(indent="  "))
# Save another copy which will not be overwritten, when rerun on another day
name = "bibliocon23-" + str(date.today()) + ".xml"
with open(name, 'w', encoding="utf-8") as outfile:
    outfile.write(reparsed.toprettyxml(indent="  "))
# Inspect differences in the output files with e.g. git diff
