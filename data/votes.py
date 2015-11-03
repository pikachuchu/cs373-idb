#!/usr/bin/env python3
import requests
import os
import json

apikey = os.environ.get('SUNLIGHT_API_KEY')

bill_data = json.load(open('bill_data.json'))
rep_data = json.load(open('rep_data.json'))

bill_ids = {}
for c in bill_data:
    curr = bill_data[c]
    bill_ids[curr['bill_id']] = c
print(bill_ids)

formatted_result = {}
for r in rep_data:
    votes = rep_data[r]['votes']
    for c in votes:
        formatted_result[(r, bill_ids[c['bill_id']])] = c['result']

result = []
for a,b in formatted_result:
    result.append([a,b,formatted_result[(a,b)]]) 

with open('votes_data.json', 'w') as outfile:
    json.dump(result, outfile)

print(result)

