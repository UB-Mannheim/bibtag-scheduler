#!/usr/bin/env python3

from datetime import date, datetime
from pathlib import Path
import html
import json
import urllib.parse
from xml.dom import minidom

from pentabarf.Conference import Conference
from pentabarf.Day import Day
from pentabarf.Event import Event
from pentabarf.Person import Person
from pentabarf.Room import Room

conference = Conference(
    title="Bibliothekskongress 2022",
    start=date(2022, 5, 31),
    end=date(2022, 6, 2),
    days=3,
    timeslot_duration="00:30",
    venue="Congress Center Leipzig",
    city="Leipzig"
)

twitterHandles = {}
if Path('cache/twitterhandles.json').is_file():
    with open('cache/twitterhandles.json') as twitterFile:
        twitterData = json.load(twitterFile)
        for user in twitterData:
            if user["name"] in twitterHandles:
                print("WARNING: Found another twitter user with the same name", user["name"])
            twitterHandles[user["name"]] = user["screen_name"]

with open("cache/bibtag22-index.json") as file:
    data = json.load(file)
    allDays = ["2022-05-31", "2022-06-01", "2022-06-02"]
    differentDays = [x['day']['date'] for x in data if x['day']['date'] not in allDays]
    if len(differentDays) > 0:
        print("ERROR: different days are found, which has to fixed before continuing", differentDays)
        exit()
    rooms = [
        "Saal 1 (mit Streaming)",
        "Saal 2 (mit Streaming)",
        "Saal 3",
        "Saal 4",
        "Saal 5",
        "Seminarraum 6/7",
        "Seminarraum 8",
        "#Freiraum22",
        "Vortragsraum 9 (mit Streaming)",
        "Vortragsraum 10",
        "Vortragsraum 11",
        "Vortragsraum 12",
        "Seminarraum 13",
        "Seminarraum 14/15",
        "M3 (Messehaus)",
        "M5 (Messehaus)",
        "Beratungsraum 3",
        "Bankettraum 4",
        "Außerhalb",
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

                                    # add the prefix "S" with session id to the title of the presentations
                                    if len(startingTimes) > 1:
                                        title = "S" + str(session['id']) + ": " + html.unescape(presentationData['title'])
                                    else:
                                        title = html.unescape(presentationData['title'])

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
                                        sessionUrl = "https://bid2022.abstractserver.com/program/#/details/sessions/" + session['id']
                                        abstract = "Session: <a href='" + sessionUrl + "'>" + session['title'] + " (S" + session['id'] + ")</a><br/><br/>"
                                        #if session['content']['outline'] is not None:
                                        #    print('WARN: outline for this session is ignored', session['id'], session['content']['outline'])

                                    abstractAdded = False
                                    if Path('cache/p' + str(presentationData['id']) + '.json').is_file():
                                        with open('cache/p' + str(presentationData['id']) + '.json') as presentationFile:
                                            presentationFileData = json.load(presentationFile)[0]
                                            if 'abstract_enriched' in presentationFileData:
                                                abstract += presentationFileData['abstract_enriched']
                                                abstractAdded = True
                                    if not abstractAdded and len(startingTimes) == 1:
                                        if session['content']['outline'] is not None:
                                            abstract = session['content']['outline']

                                    presentationObject = Event(
                                        id='p' + str(presentationData['id']),
                                        date=datetime.fromisoformat(dayText + "T" + start + ":00+02:00"),
                                        start=start,
                                        duration='%02d:%02d' % (hoursDiff, minutesDiff),
                                        track=session['session_type']['name'],
                                        abstract=abstract,
                                        title=title,
                                        type='Vortrag'
                                    )

                                    personList = []
                                    for author in presentationData['persons']:
                                        authorName = author['person']['first_name'] + ' ' + author['person']['last_name']
                                        if authorName in twitterHandles:
                                            personList.append("@" + twitterHandles[authorName.strip()])
                                        else:
                                            personList.append(authorName)
                                        person = Person(name=authorName, id=author['person']['id'])
                                        presentationObject.add_person(person)
                                    tweetContent = urllib.parse.quote_plus(html.unescape(presentationData['title']) + ' | ' + ", ".join(personList))
                                    presentationObject.abstract += '<p><a href="https://twitter.com/intent/tweet?hashtags=bibtag22&text=' + tweetContent + '">Tweet</a></p>'

                                    room.add_event(presentationObject)

                                eventsAdded = True
                            else:
                                print("WARNING: Found several presentations at the same time in this session", session['id'], session['title'], session['session_type']['name'])
                                # create an abstract for the whole session which will be added below
                                abstract = "<ul>"
                                for presentationData in sessionData['presentations']:
                                    abstract += "<li>" + presentationData['start_time'] + "-" + presentationData['end_time'] + ": " + presentationData['title']
                                    if 'persons' in presentationData:
                                        for author in presentationData['persons']:
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


with open("bibtag22.xml", 'w', encoding="utf-8") as outfile:
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
    outfile.write(reparsed.toprettyxml(indent="  "))
