#!/usr/bin/env python3
import requests
import os
import json

apikey = os.environ.get('SUNLIGHT_API_KEY')

committee_data = json.load(open('committee_data.json'))
rep_data = json.load(open('rep_data.json'))

print(len(committee_data))
committee_ids = {}
for c in committee_data:
    curr = committee_data[c]
    committee_ids[curr['committee_id']] = c

formatted_result = [] 
for r in rep_data:
    committees = rep_data[r]['committees']
    for c in committees:
        formatted_result.append([r, committee_ids[c['id']]])

with open('committee_members_data.json', 'w') as outfile:
    json.dump(formatted_result, outfile)
print(formatted_result)

