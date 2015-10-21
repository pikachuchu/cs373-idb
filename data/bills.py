import json
import os
import requests

apikey = os.environ.get('SUNLIGHT_API_KEY')
sunlight_url = 'http://congress.api.sunlightfoundation.com/bills?apikey=' + apikey + '&history.active=true&order=last_action_at&history.house_passage_result__exists=true&history.senate_passage_result__exists=true'

committee_data = json.load(open('committee_data.json'))

formatted = {}
for k in committee_data:
    curr_url = sunlight_url + '&committee_ids=' + k
    results = requests.get(curr_url).json()['results']
    if len(results) == 0:
        print(k)
    for i in range(min(5,len(results))):
        curr = results[i]
        name = curr['short_title']
        if not name:
            name = curr['official_title']
        obj = {
            "id": curr['bill_id'],
            "name": name,
            "date_introduced": curr['introduced_on'],
            "house_status": curr['history']['house_passage_result'],
            "senate_status": curr['history']['senate_passage_result'],
            "committees": curr['committee_ids']
        }
        sponsor_url = 'http://congress.api.sunlightfoundation.com/legislators?apikey=' + apikey + '&bioguide_id=' + curr['sponsor_id']
        sponsor = requests.get(sponsor_url).json()['results']
        if len(sponsor) > 0:
            sponsor = sponsor[0]
            obj['sponsor'] = {
                'name': sponsor['first_name'] + ' ' + sponsor['last_name'],
                'id': sponsor['govtrack_id']
            }
        formatted[curr['bill_id']] = obj

with open('bill_data.json', 'w') as outfile:
    json.dump(formatted, outfile)
