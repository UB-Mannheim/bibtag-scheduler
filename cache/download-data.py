#!/usr/bin/env python3

import json
import requests
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

apiUrl = 'https://www.professionalabstracts.com/api/iplanner/index.php?'
indexUrl = apiUrl + 'conf=dbt2020&method=get&model=index'
sessionUrl = apiUrl + 'conf=dbt2020&method=get&model=sessions&params[sids]='
presentationUrl = apiUrl + 'conf=dbt2020&method=get&model=presentation&params[pid]='

# download main data
req = requests.get(indexUrl, verify=False)
data = req.json()
with open('bibtag20-index.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

# download details of all sessions
presentationIds = []
for sessionId in data['match']:
    time.sleep(2)
    print("Download session details for", sessionId)
    req = requests.get(sessionUrl + sessionId, verify=False)
    data = req.json()
    with open('s' + sessionId + '.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    if 'pres' in data['1']:
        for presentation in data['1']['pres']:
            presentationIds.append(data['1']['pres'][presentation]['id'])
with open('presentationtIds', 'w') as outfile:
    json.dump(presentationIds, outfile, indent=4)

# download details of all presentations
for presentationId in presentationIds:
    time.sleep(2)
    print("Download presentation details for", presentationId)
    req = requests.get(presentationUrl + str(presentationId), verify=False)
    data = req.json()
    with open('p' + str(presentationId) + '.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
