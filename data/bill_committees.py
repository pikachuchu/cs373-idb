#!/usr/bin/env python3
import requests
import os
import json

apikey = os.environ.get('SUNLIGHT_API_KEY')

bill_data = json.load(open('bill_data.json'))
committee_data = json.load(open('committee_data.json'))

committee_ids = {}
for c in committee_data:
    curr = committee_data[c]
    committee_ids[curr['committee_id']] = c

formatted_result = []
for r in bill_data:
    committees = bill_data[r]['committees']
    for c in committees:
        try:
            formatted_result.append([r, committee_ids[c]])
        except:
            pass

with open('bill_committee_data.json', 'w') as outfile:
    json.dump(formatted_result, outfile)

print(formatted_result)

