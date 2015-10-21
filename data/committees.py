import os
import requests
import json

govtrack_url = 'https://www.govtrack.us/api/v2/committee?limit=228&obsolete=false'
committees = requests.get(govtrack_url).json()['objects']
people_data = json.load(open('rep_data.json'))
apikey = os.environ.get('SUNLIGHT_API_KEY')

formatted = {}
for v in committees:
    curr = v['committee']
    if not curr:
        curr = v
    obj = {
        "id": curr['code'],
        "name": curr['name'],
        "website": curr['url'],
        "chamber": curr['committee_type'],
        "jurisdiction": curr['jurisdiction']
    }

    sunlight_url = 'http://congress.api.sunlightfoundation.com/committees?apikey=' + apikey + '&committee_id=' + curr['code'] + '&fields=members'
    members = requests.get(sunlight_url).json()['results'][0]['members']
    chairperson = members[0]
    if chairperson['title'] == 'Chairman':
        chair = chairperson['legislator']
        obj['chair'] = {
            'name': chair['first_name'] + ' ' + chair['last_name'],
            'id': chair['govtrack_id']
        }
    formatted[curr['code']] = obj

with open('committee_data.json', 'w') as outfile:
    json.dump(formatted, outfile)

