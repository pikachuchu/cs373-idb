from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import json
from models import rep, bill, committee

engine = create_engine('mysql+mysqldb://root:politicianhub@localhost/test')
Session = sessionmaker(bind=engine)
session = Session()

bio_to_id = {}

with open('data/rep_data.json', 'r') as infile:
	 data = json.load(infile)

for key in data:	
	info = data[key]
	bio_to_id[info['bioguide_id']] = info['id']
	curr_rep = rep(
		id = info['id'],
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

blacklist = set()

for key in data:	
	info = data[key]
	if 'sponsor' not in info:
		blacklist.add(info['id'])
		continue
	cur_bill = bill(
		id = info['id'],
		name = info['name'],
		date_intro = info['date_introduced'],
		house_status = info['house_status'],
		senate_status = info['senate_status'],
		#fk_sponsor = bio_to_id[info['sponsor']['id']],
		fk_sponsor = 1,
		voting_url = info['link'])
	session.add(cur_bill)

with open('data/committee_data.json', 'r') as infile:
	 data = json.load(infile)

for key in data:	
	info = data[key]
	if 'chair' not in info:
		continue
	cur_com = committee(
		id = info['id'],
		name = info['name'],
		chamber = info['chamber'],
		website = info['website'],
		jurisdiction = info['jurisdiction'],
		fk_chair = 1)
		#fk_chair = bio_to_id[info['chair']['id']])
	session.add(cur_com)

session.commit()
