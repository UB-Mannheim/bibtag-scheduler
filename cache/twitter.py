#!/usr/bin/env python3

import json

from pathlib import Path

import tweepy


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
i = 0
for user in members:
    print(i)
    i += 1
    data.append(user._json)

with open('twitterhandles.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
