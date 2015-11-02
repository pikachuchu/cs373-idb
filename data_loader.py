from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import json
from models import legislator, bill, committee, committee_member, vote, bill_committee

engine = create_engine('mysql+mysqldb://root:politicianhub@localhost/phub?charset=utf8')
Session = sessionmaker(bind=engine)
session = Session()
engine.echo = True

bio_to_id = {}

with open('data/rep_data.json', 'r') as infile:
	 data = json.load(infile)

for key in data:	
	info = data[key]
	bio_to_id[info['bioguide_id']] = info['id']
	curr_rep = legislator(
		id = key,
		first_name = info['first_name'],
		last_name = info['last_name'], 
		chamber = info['chamber'],
		gender = info['gender'],
		birthday = info['birthday'],
		party = info['party'],
		state = info['state'],
		twitter = info['twitter'],
		website = info['website'],
		bio_guide = info['bioguide_id'],
		contact_form = info['contact_form'],
		image = info['image_jpg'])
	session.merge(curr_rep)


with open('data/bill_data.json', 'r') as infile:
	 data = json.load(infile)

for key in data:	
    info = data[key]
    if 'sponsor' in info:
        sponsor = bio_to_id[info['sponsor']['id']]
    else:
        sponsor = None
    cur_bill = bill(
        id = key,
        name = info['name'],
        bill_type = info['bill_type'],
        bill_id = info['bill_id'],
        date_intro = info['date_introduced'],
        house_status = info['house_status'],
        senate_status = info['senate_status'],
        link = info['link'],
        current_status_label = info['current_status_label'],
        current_status_description = info['current_status_description'],
        current_status = info['current_status'],
        fk_sponsor = sponsor)

    session.add(cur_bill)

with open('data/committee_data.json', 'r') as infile:
	 data = json.load(infile)

for key in data:	
    info = data[key]
    if 'chair' in info:
        chair = bio_to_id[info['chair']['id']]
    else:
        chair = None
    cur_com = committee(
        id = key,
        name = info['name'],
        chamber = info['chamber'],
        website = info['website'],
        jurisdiction = info['jurisdiction'],
        is_subcommittee = info['is_subcommittee'],
        committee_id = info['committee_id'],
        fk_chair = chair)
    session.add(cur_com)

data = json.load(open('data/committee_members_data.json'))
for l,c in data:
    curr = committee_member(
        legislator_id = int(l),
        committee_id = int(c)
    )
    session.add(curr)

data = json.load(open('data/votes_data.json'))
for l,b,r in data:
    curr = vote(
        legislator_id = int(l),
        bill_id = int(b),
        result = r
    )
    session.add(curr)

data = json.load(open('data/bill_committee_data.json'))
for b,c in data:
    curr = bill_committee(
        bill_id = int(b),
        committee_id = int(c)
    )
    session.add(curr)

session.commit()

