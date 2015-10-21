#!/usr/bin/env python3
import requests
import os
import json

apikey = os.environ.get('SUNLIGHT_API_KEY')

## id, first_name, last_name, chamber, gender, birthday, party, state, twitter, youtube, website, contact_form, committees
govtrack_url = 'https://www.govtrack.us/api/v2/role?current=true&limit=543'
govtrack_result = requests.get(govtrack_url).json()['objects']
base_image_url = 'https://raw.githubusercontent.com/unitedstates/images/gh-pages/congress/450x550/'

formatted_result = {}
for v in govtrack_result:
    # govtrack stuff
    person = v['person']
    roletype = v['role_type']
    if roletype == 'representative':
        roletype = 'house'
    contact_form = ''
    if 'contact_form' in v['extra']:
        contact_form = v['extra']['contact_form']
    obj = {
        "id": person['id'],
        "first_name": person['firstname'],
        "last_name": person['lastname'],
        "chamber": roletype,
        "gender": person['gender'],
        "birthday": person['birthday'],
        "state": v['state'],
        "party": v['party'],
        "twitter": person['twitterid'],
        "youtube": person['youtubeid'],
        "website": v['website'],
        "contact_form": contact_form
    }

    # get image url
    image_id = person['bioguideid']
    image_url = base_image_url + image_id + '.jpg'
    image_req = requests.get(image_url)
    if image_req.status_code == 200:
        obj['image_jpg'] = image_url
    else:
        print(person['firstname'] + ' ' + person['lastname'])

    # sunlight committee stuff
    sunlight_url = 'http://congress.api.sunlightfoundation.com/legislators?apikey=' + apikey + '&last_name=' + person['lastname']
    bioguide_arr = requests.get(sunlight_url).json()['results']
    if len(bioguide_arr) > 0:
        bioguide_id = bioguide_arr[0]['bioguide_id']
        committee_url = 'http://congress.api.sunlightfoundation.com/committees?apikey=' + apikey + '&member_ids=' + bioguide_id
        committees = requests.get(committee_url).json()['results']

        committee_list = []
        for v in committees:
            committee_list.append({
                'id': v['committee_id'], 
                'name': v['name']
            })
        obj['committees'] = committee_list

    formatted_result[person['id']] = obj

with open('rep_data.json', 'w') as outfile:
    json.dump(formatted_result, outfile)

print(formatted_result[400034])


