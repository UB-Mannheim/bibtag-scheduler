#!/usr/bin/env python3

import json
import requests
import time
import urllib3

from pathlib import Path
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEBUG = False
numberOfDays = 4
apiUrl = 'https://bibliocon2024.planner.documedias.systems/api/'

# Previous years
# apiUrl = 'https://dbt2023.planner.documedias.systems/api'
# apiUrl = 'https://bid2022.planner.documedias.systems/api'

sessionUrl = apiUrl + '/program/sessions/'
presentationUrl = apiUrl + '/program/presentations/'

# More URLs examples:
# Days:
#    https://bibliocon2024.planner.documedias.systems/api/program/days/1
#    https://bibliocon2024.planner.documedias.systems/api/program/days/2
#    https://bibliocon2024.planner.documedias.systems/api/program/days/3
#    https://bibliocon2024.planner.documedias.systems/api/program/days/4
# One Session:
#    https://bibliocon2024.planner.documedias.systems/api/program/sessions/175
# One Presentation:
#    https://bibliocon2024.planner.documedias.systems/api/program/presentations/114
# Abstract (will be handled later):
#    https://bibliocon2024.abstract.documedias.systems/api/v1/manager/abstract/multi/html/id/252/template/planner_preview
# Rooms:
#    https://bibliocon2024.planner.documedias.systems/api/program/rooms/2
# Options:
#    https://bibliocon2024.planner.documedias.systems/api/program/options



# reliably open a file in the same directory as the current script
p = Path(__file__)

# download main data
with p.with_name('index.json').open('w') as outfile:
    data = []
    for day in range(1, numberOfDays + 1):
        req = requests.get(apiUrl + "/program/days/" + str(day), verify=False)
        data += req.json()

    json.dump(data, outfile, indent=4)

# download rooms (for every day individually)
with p.with_name('rooms.json').open('w') as outfile:
    rooms_data = []
    ids = []
    for day in range(1, numberOfDays + 1):
        req = requests.get(apiUrl + "/program/rooms/" + str(day), verify=False)
        for element in req.json():
            if element['id'] not in ids:
                rooms_data += [element]
                ids += [element['id']]
    json.dump(rooms_data, outfile, indent=4)

# download details of all sessions
presentationIds = []
now = datetime.now()
print(now.strftime("%H:%M"), "Download details for all sessions. Expected time for that is at least", 2*len(data)/60, "minutes.")
for session in data:
    sessionId = str(session["id"])
    time.sleep(2)
    if DEBUG:
        print("Download session details for", sessionId)
    req = requests.get(sessionUrl + sessionId, verify=False)
    data = req.json()
    if len(data) > 1:
        print("Unexpected format for session" + sessionId)
    with p.with_name('s' + sessionId + '.json').open('w') as outfile:
        json.dump(data, outfile, indent=4)
    if 'presentations' in data[0]:
        for presentation in data[0]['presentations']:
            presentationIds.append(presentation["presentation"]["id"])

with p.with_name('presentationtIds').open('w') as outfile:
    json.dump(presentationIds, outfile, indent=4)

# download details of all presentations
now = datetime.now()
print(now.strftime("%H:%M"), "Download details for all presentations. Expected time for that is at least", 2*len(presentationIds)/60, "minutes.")
for presentationId in presentationIds:
    time.sleep(2)
    if DEBUG:
        print("Download presentation details for", presentationId)
    req = requests.get(presentationUrl + str(presentationId), verify=False)
    if not req:
        print("Failure", req.status_code, "for downloading presentation detail for", presentationId)
        continue
    data = req.json()
    if len(data) > 1:
        print("Unexpected format for presentation" + presentationId)
    abstractId = str(data[0]["abstract_id"])
    if abstractId != "None":
        abstractUrl = apiUrl.replace(".planner.", ".abstract.") + "/v1/manager/abstract/multi/html/id/" + abstractId + "/template/planner_preview"
        req = requests.get(abstractUrl, verify=False)
        if req.status_code == 200:
            dataAbstract = req.json()
            if abstractId not in dataAbstract:
                print("Unexpected format for abstract" + abstractId)
            else:
                data[0]["abstract_enriched"] = dataAbstract[abstractId]
        else:
            print(req.status_code, "Error when requesting the abstract", abstractUrl, "for presentation", presentationId, data[0]["title"])
    with p.with_name('p' + str(presentationId) + '.json').open('w') as outfile:
        json.dump(data, outfile, indent=4)

now = datetime.now()
print(now.strftime("%H:%M"), "Done")
