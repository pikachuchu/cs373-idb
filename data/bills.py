import json
import os
import requests

apikey = os.environ.get('SUNLIGHT_API_KEY')
sunlight_url = 'http://congress.api.sunlightfoundation.com/bills?apikey=' + apikey + '&history.active=true&order=last_action_at&history.house_passage_result__exists=true&history.senate_passage_result__exists=true'

bill_types = {
    'hr': 'house_bill',
    'hres': 'house_resolution',
    'hjres': 'house_joint_resolution',
    'hconres': 'house_concurrent_resolution',
    's': 'senate_bill',
    'sres': 'senate_resolution',
    'sjres': 'senate_joint_resolution',
    'sconres': 'senate_concurrent_resolution'
}

committee_data = json.load(open('committee_data.json'))
rep_data = json.load(open('rep_data.json'))

formatted = {}

def get_bill(bill_id):
    url = 'http://congress.api.sunlightfoundation.com/bills?apikey=' + apikey + '&bill_id=' + bill_id
    bill = requests.get(url).json()['results'][0]
    name = bill['short_title']
    if not name:
        name = bill['official_title']
    if 'house_passage_result' in bill['history']:
        house_status = bill['history']['house_passage_result']
    else:
        house_status = ''
    if 'senate_passage_result' in bill['history']:
        senate_status = bill['history']['senate_passage_result']
    else:
        senate_status = ''
    obj = {
        "bill_id": bill['bill_id'],
        "name": name,
        "date_introduced": bill['introduced_on'],
        "house_status": house_status,
        "senate_status": senate_status,
        "committees": bill['committee_ids']
    }
    sponsor_url = 'http://congress.api.sunlightfoundation.com/legislators?apikey=' + apikey + '&bioguide_id=' + bill['sponsor_id']
    sponsor = requests.get(sponsor_url).json()['results']
    if len(sponsor) > 0:
        sponsor = sponsor[0]
        obj['sponsor'] = {
            'name': sponsor['first_name'] + ' ' + sponsor['last_name'],
            'id': sponsor['bioguide_id']
        }

    # govtrack
    bill_type = bill_types[bill['bill_type']]
    number = bill['number']
    congress = bill['congress']
    govtrack_url = 'https://www.govtrack.us/api/v2/bill?bill_type=' + bill_type + '&number=' + str(number) + '&congress=' + str(congress)
    govtrack_bill = requests.get(govtrack_url).json()['objects'][0]
    obj['current_status'] = govtrack_bill['current_status']
    obj["current_status_description"] = govtrack_bill['current_status_description']
    obj["current_status_label"] = govtrack_bill['current_status_label']
    obj["link"] = govtrack_bill['link']
    obj["bill_type"] = govtrack_bill['bill_type']

    formatted[bill_id] = obj

for k in rep_data:
    print(k)
    for v in rep_data[k]['votes']:
        # sunlight
        bill_id = v['bill_id']
        get_bill(bill_id)

for k in committee_data:
    print(k)
    committee_id = committee_data[k]['committee_id']
    curr_url = sunlight_url + '&committee_ids=' + committee_id
    results = requests.get(curr_url).json()['results']
    if len(results) == 0:
        print(committee_id)
    for i in range(min(5,len(results))):
        curr = results[i]
        get_bill(curr['bill_id'])

num = 0
result = {}
for v in formatted:
    obj = formatted[v]
    obj['id'] = num
    result[num] = obj
    num += 1

with open('bill_data.json', 'w') as outfile:
    json.dump(result, outfile)

print(result[0])
