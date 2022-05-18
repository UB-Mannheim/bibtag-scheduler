#!/usr/bin/env python3

import json
import requests
import time
import urllib3

from pathlib import Path

import tweepy

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

numberOfDays = 3
apiUrl = 'https://bid2022.planner.documedias.systems/api'
#https://bid2022.planner.documedias.systems/api/program/days/1
#https://bid2022.planner.documedias.systems/api/program/days/2
#https://bid2022.planner.documedias.systems/api/program/days/3
sessionUrl = apiUrl + '/program/sessions/'
#https://bid2022.planner.documedias.systems/api/program/sessions/130
presentationUrl = apiUrl + '/program/presentations/'
#https://bid2022.planner.documedias.systems/api/program/presentations/191
#abstractUrl =
# https://bid2022.abstract.documedias.systems/api/v1/manager/abstract/multi/html/id/188/template/planner_preview

# https://bid2022.planner.documedias.systems/api/program/rooms
# https://bid2022.planner.documedias.systems/api/program/options

# download main data

with open('bibtag22-index.json', 'w') as outfile:
    data = []
    for day in range(1, numberOfDays + 1):
        req = requests.get(apiUrl + "/program/days/" + str(day), verify=False)
        data += req.json()

    json.dump(data, outfile, indent=4)

# download details of all sessions
presentationIds = []
for session in data:
    sessionId = str(session["id"])
    time.sleep(2)
    print("Download session details for", sessionId)
    req = requests.get(sessionUrl + sessionId, verify=False)
    data = req.json()
    if len(data) > 1:
        print("Unexpected format for session" + sessionId)
    with open('s' + sessionId + '.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    if 'presentations' in data[0]:
        for presentation in data[0]['presentations']:
            presentationIds.append(presentation["id"])

with open('presentationtIds', 'w') as outfile:
    json.dump(presentationIds, outfile, indent=4)

# download details of all presentations
for presentationId in presentationIds:
    time.sleep(2)
    print("Download presentation details for", presentationId)
    req = requests.get(presentationUrl + str(presentationId), verify=False)
    data = req.json()
    if len(data) > 1:
        print("Unexpected format for presentation" + presentationId)
    abstractId = str(data[0]["abstract_id"])
    abstractUrl = "https://bid2022.abstract.documedias.systems/api/v1/manager/abstract/multi/html/id/" + abstractId + "/template/planner_preview"
    req = requests.get(abstractUrl, verify=False)
    if req.status_code == 200:
        dataAbstract = req.json()
        if abstractId not in dataAbstract:
            print("Unexpected format for abstract" + abstractId)
        else:
            abstract = dataAbstract[abstractId]
            data[0]["abstract_enriched"] = abstract
    else:
        print(req.status_code, "Error when requesting the abstract", abstractUrl, "for presentation", presentationId, data[0]["title"])
    with open('p' + str(presentationId) + '.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

# download twitter data from the collected list of twitter handles by @bibliothekarin
# https://twitter.com/i/lists/1518677854812258304/members
if Path('twittercredentials.json').is_file():
    with open('twittercredentials.json', 'r') as infile:
        CREDENTIALS = json.load(infile)
else:
    print("ERROR: no file twittercredentials.json found.",
          "You have to create such a file and save your twitter credentials there.")
    exit(1)

auth = tweepy.OAuthHandler(CREDENTIALS["consumerKey"], CREDENTIALS["consumerSecret"])
auth.set_access_token(CREDENTIALS["accessToken"], CREDENTIALS["accessSecret"])
api = tweepy.API(auth)
api.verify_credentials()

data = []
members = api.get_list_members(list_id=1518677854812258304, count=500)
for user in members:
    data.append(user._json)

with open('twitterhandles.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
