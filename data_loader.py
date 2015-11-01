from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import json
from models import rep

engine = create_engine('mysql+mysqldb://root:politicianhub@localhost/phub')
Session = sessionmaker(bind=engine)
session = Session()


with open('rep_data.json', 'r') as infile:
	data = json.load(infile)

s = set()
for key in data:	
	if key in s:
		print key
		continue
	else:
		s.add(key)
	info = data[key]
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
	session.add(curr_rep)

session.commit()
