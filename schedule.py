#!/usr/bin/env python3

from datetime import date, datetime
from pathlib import Path
import html
import json
import re
from xml.dom import minidom

from pentabarf.Conference import Conference
from pentabarf.Day import Day
from pentabarf.Event import Event
from pentabarf.Person import Person
from pentabarf.Room import Room

conference = Conference(
    title="Bibliothekartag 2020",
    start=date(2020, 5, 26),
    end=date(2020, 5, 29),
    days=4,
    timeslot_duration="00:30",
    venue="Hannover Congress Centrum (HCC)",
    city="Hannover"
)

with open("cache/bibtag20-index.json") as file:
    data = json.load(file)
    for timestamp in data['groups']:
        day = Day(date=date.fromtimestamp(int(timestamp)))

        rooms = [x['room'] for x in data['sessions'][timestamp]]

        for roomName in list(dict.fromkeys(rooms)):
            room = Room(name=roomName)
            correspondingSessions = [x for x in data['sessions'][timestamp] if x['room'] == roomName]
            for session in correspondingSessions:
                abstract = None

                type = session['type']
                if session['type'].startswith('Themenkreis'):
                    type = "Vortragssession"
                if session['type'].startswith('Hands-On Lab'):
                    type = "Hands-On Lab"

                eventsAdded = False
                # try to add the presentations instead of the complete session
                # thus first check whether there are some additional data for this session
                if Path('cache/s' + session['id'] + '.json').is_file():
                    with open('cache/s' + session['id'] + '.json') as sessionFile:
                        sessionData = json.load(sessionFile)
                        if 'pres' in sessionData['1']:

                            # copy the outline to the session such that it can also be used if there are no
                            # presentation to add
                            if 'outline' in sessionData['1']:
                                session['outline'] = sessionData['1']['outline']

                            # For Podiumsdiskussion the Diskutantent are saved in an additional presentation, which we
                            # try to recognize here, save the information in a variable, and then delete this node.
                            # Because most of the time there is the other presentation which we should treat as a single
                            # presentation.
                            diskutantenText = "Diskutanten: "
                            if sessionData['1']['type'] == "Podiumsdiskussion":
                                for pres in sessionData['1']['pres']:
                                    if sessionData['1']['pres'][pres]['title'] == "Diskutanten":
                                        diskutanten = sessionData['1']['pres'][pres]
                                        if 'pers' in diskutanten:
                                            diskutantenArray = [diskutanten['pers'][x]['text']  for x in diskutanten['pers']]
                                            diskutantenText += "; ".join(diskutantenArray)
                                        del sessionData['1']['pres'][pres]
                                        break

                            # for some sessions e.g. 62 there are several presentations at the same time, which looks more
                            # like an error or some unusual pattern, and therefore we better don't take the individual
                            # presentations but hte whole session
                            startingTimes = [sessionData['1']['pres'][x]['frame'][:5] for x in sessionData['1']['pres']]
                            if len(startingTimes) == len(list(dict.fromkeys(startingTimes))):

                                for pres in sessionData['1']['pres']:
                                    presentationData = sessionData['1']['pres'][pres]

                                    # add the prefix "S" with session id to the title of the presentations
                                    if len(startingTimes) > 1:
                                        title = "S" + session['id'] + ": " + html.unescape(presentationData['titleplain'])
                                    else:
                                        title = html.unescape(presentationData['titleplain'])

                                    start = presentationData['frame'][:5]
                                    end = presentationData['frame'][6:11]
                                    hoursDiff = int(end[:2]) - int(start[:2])
                                    minutesDiff = int(end[3:5]) - int(start[3:5])
                                    if minutesDiff < 0:
                                        hoursDiff -= 1
                                        minutesDiff += 60

                                    if len(startingTimes) > 1:
                                        abstract = "Session: " + session['title'] + " (S" + session['id'] + ")<br/><br/>"
                                        if 'outline' in session and len(session['outline']) > 0:
                                            print('WARN: outline for this session is ignored', session['id'], session['outline'])
                                    else:
                                        if 'outline' in session and len(session['outline']) > 0:
                                            abstract = session['outline'] + "<br/><br/>"
                                        else:
                                            abstract = ""
                                    if len(diskutantenText) > 16:
                                        abstract += diskutantenText + ")<br/><br/>"
                                    if Path('cache/p' + str(presentationData['id']) + '.json').is_file():
                                        with open('cache/p' + str(presentationData['id']) + '.json') as presentationFile:
                                            presentationFileData = json.load(presentationFile)
                                            abstract += presentationFileData['text']
                                            abstract += "<br/><br/>" + presentationFileData['aut']
                                            abstract += "<br/>" + presentationFileData['inst']

                                    presentationObject = Event(
                                        id='p' + str(presentationData['id']),
                                        date=date.fromtimestamp(int(timestamp)),
                                        start=start,
                                        duration='%02d:%02d' % (hoursDiff, minutesDiff),
                                        track=session['type'],
                                        abstract=abstract,
                                        title=title,
                                        type='Vortrag',
                                        # TODO is this useful at all?
                                        conf_url='https://www.professionalabstracts.com/dbt2020/iplanner/#/presentation/'
                                                 + str(presentationData['id'])
                                    )

                                    if 'aut' in presentationData:
                                        cleanr = re.compile('</?u>|<sup>\d+(,\s*\d+)*</sup>')
                                        authors = re.sub(cleanr, '', presentationData['aut']).split(',')

                                        for author in authors:
                                            person = Person(name=author.strip())
                                            presentationObject.add_person(person)

                                    room.add_event(presentationObject)

                                eventsAdded = True
                            else:
                                print("WARNING: Found several presentations at the same time in this session", session['id'], session['title'], session['type'])
                                # create an abstract for the whole session which will be added below
                                abstract = ""
                                for pres in sessionData['1']['pres']:
                                    presentationData = sessionData['1']['pres'][pres]
                                    abstract += presentationData['titleplain']
                                    if 'pers' in presentationData:
                                        for person in presentationData['pers']:
                                            abstract += '<br/>' + presentationData['pers'][person]['text']
                                    abstract += '<br/><br/>'



                            endingTimes = [sessionData['1']['pres'][x]['frame'][6:11] for x in sessionData['1']['pres']]
                            if session['end'] not in endingTimes:
                                print("WARNING: Session goes longer than any presentation", session['id'], session['title'], session['date'], session['time'])

                # add event for the whole session when no events are yet added
                if not eventsAdded:

                    if 'outline' in session and len(session['outline']) > 0:
                        abstract = session['outline']
                    sessionObject = Event(
                        id=session['id'],
                        date=date.fromtimestamp(int(timestamp)),
                        start=session['start'],
                        duration='%02d:%02d' % ((int(session['length']) // 60), (int(session['length']) % 60)),
                        track=session['type'],
                        abstract=abstract,
                        title=html.unescape(session['title']),
                        type=type,
                    )

                    if sessionData and 'pers' in sessionData['1']:
                        for author in sessionData['1']['pers']:
                            person = Person(name=sessionData['1']['pers'][author]['text'].split(',')[0])
                            sessionObject.add_person(person)

                    room.add_event(sessionObject)

            day.add_room(room)

        conference.add_day(day)


with open("output.xml", 'w', encoding="utf-8") as outfile:
    xmldata = conference.generate("Erzeugt von bibtag-scheduler um " + str(datetime.now()))
    reparsed = minidom.parseString(xmldata.decode("utf-8"))
    # delete day_change as it cannot be empty
    for node in reparsed.getElementsByTagName('day_change'):
        node.parentNode.removeChild(node)
    # use links/link instead of conf_url
    for node in reparsed.getElementsByTagName('conf_url'):
        if len(node.toxml()[10:-11]) > 0:
            linksNode = reparsed.createElement('links')
            node.parentNode.appendChild(linksNode)
            linkNode = reparsed.createElement('link')
            linksNode.appendChild(linkNode)
            linkNode.setAttribute('href', node.toxml()[10:-11])
            textNode = reparsed.createTextNode('DBT2020')
            linkNode.appendChild(textNode)
            node.parentNode.removeChild(node)
    # delete some empty nodes and empty attributes
    deleted = 0
    for ignore in ['description', 'conf_url', 'full_conf_url', 'released']:
        for node in reparsed.getElementsByTagName(ignore):
            if node.toxml() == "<" + ignore + "/>":
                node.parentNode.removeChild(node)
                deleted += 1
    print("INFO: Deleted", deleted, "empty nodes")
    for node in reparsed.getElementsByTagName('person'):
        if node.getAttribute('id') == "None":
            node.removeAttribute('id')
    outfile.write(reparsed.toprettyxml(indent="  "))
