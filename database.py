from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from models import rep

db = create_engine('mysql+mysqldb://root:politicianhub@localhost/phub')
Session = sessionmaker(bind=db)
session = Session()

def create_legislator_obj(row):
    return {
        'id': row.id,
        'first_name': row.first_name,
        'last_name': row.last_name,
        'chamber': row.chamber,
        'gender': row.gender,
        'birthday': row.birthday,
        'party': row.party,
        'state': row.state,
        'twitter': row.twitter,
        'website': row.website,
        'bio_guide': row.bio_guide,
        'contact_form': row.contact_form,
        'image': row.image
    }
    # TODO: add committee data

"""
Get all legislators from the database
"""
def get_legislators():
    result = []
    for row in session.query(rep).order_by(rep.id):
        obj = create_legislator_obj(row)
        result.append(obj)
    return result

"""
Get all committees from the database
"""
def get_committees():
    pass

"""
Get all bills from the database
"""
def get_bills():
    pass

"""
Get a legislator by its id from the database
"""
def get_legislator_by_id(legislator_id):
    row = session.query(rep).filter(rep.id == legislator_id).first()
    obj = create_legislator_obj(row)
    return obj

"""
Get a committee by its id from the database
"""
def get_committee_by_id(committee_id):
    pass

"""
Get a bill by its id from the database
"""
def get_bill_by_id(bill_id):
    pass

