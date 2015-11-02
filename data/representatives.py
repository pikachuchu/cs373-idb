#!/usr/bin/env python3
import requests
import os
import json

apikey = os.environ.get('SUNLIGHT_API_KEY')

## id, first_name, last_name, chamber, gender, birthday, party, state, twitter, youtube, website, contact_form, committees
govtrack_url = 'https://www.govtrack.us/api/v2/role?current=true&limit=543'
govtrack_result = requests.get(govtrack_url).json()['objects']
base_image_url = 'https://raw.githubusercontent.com/unitedstates/images/gh-pages/congress/450x550/'

num = 0
formatted_result = {}
for v in govtrack_result:
    # govtrack stuff
    person = v['person']
    roletype = v['role_type']
    if roletype == 'representative':
        roletype = 'House'
    else:
        roletype = 'Senate'
    contact_form = ''
    if 'contact_form' in v['extra']:
        contact_form = v['extra']['contact_form']
    obj = {
        "id": num,
        "bioguide_id": person['bioguideid'],
        "first_name": person['firstname'],
        "last_name": person['lastname'],
        "chamber": roletype,
        "gender": person['gender'],
        "birthday": person['birthday'],
        "state": v['state'],
        "party": v['party'],
        "twitter": person['twitterid'],
        "website": v['website'],
        "contact_form": contact_form
    }

    # get image url
    image_id = person['bioguideid']
    image_url = base_image_url + image_id + '.jpg'
    image_req = requests.get(image_url)
    if image_req.status_code == 200:
        obj['image_jpg'] = image_url
    #else:
        #print(person['firstname'] + ' ' + person['lastname'])

    # sunlight committee stuff
    committee_url = 'http://congress.api.sunlightfoundation.com/committees?apikey=' + apikey + '&member_ids=' + person['bioguideid']
    committees = requests.get(committee_url).json()['results']

    committee_list = []
    for v in committees:
        committee_list.append({
            'id': v['committee_id'],
            'name': v['name']
        })
    obj['committees'] = committee_list

    # votes
    vote_url = 'http://congress.api.sunlightfoundation.com/votes?apikey=' + apikey + '&voter_ids.' + person['bioguideid'] + '__exists=true&order=voted_at&vote_type=passage&fields=bill_id,voter_ids,voted_at' 
    votes = requests.get(vote_url).json()['results']

    votes_list = []
    for i in range(20):
        try:
            v = votes[i]
            votes_list.append({
                'bill_id': v['bill_id'],
                'date': v['voted_at'],
                'result': v['voter_ids'][person['bioguideid']]
            })
        except:
            break

    obj['votes'] = votes_list

    formatted_result[obj['id']] = obj
    num += 1

with open('rep_data.json', 'w') as outfile:
    json.dump(formatted_result, outfile)

print(formatted_result)

