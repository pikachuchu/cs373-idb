from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from models import *

db = create_engine('mysql+mysqldb://root:politicianhub@localhost/phub?charset=utf8')
Session = sessionmaker(bind=db)
session = Session()

def add_committee_members(row, obj, verbose):
    obj['committees'] = []
    for r in session.query(committee_member).filter(committee_member.legislator_id == row.id):
        if verbose:
            obj['committees'].append(get_committee_by_id(r.committee_id, verbose))
        else:
            obj['committees'].append(r.committee_id)

def add_votes(row, obj, verbose):
    obj['votes'] = []
    for r in session.query(vote).filter(vote.legislator_id == row.id):
        if verbose:
            obj['votes'].append({
                'bill': get_bill_by_id(r.bill_id, verbose),
                'result': r.result
            })
        else:
            obj['votes'].append({
                'bill_id': r.bill_id,
                'result': r.result
            })

def add_bill_committees(row, obj, verbose):
    obj['committees'] = []
    for r in session.query(bill_committee).filter(bill_committee.bill_id == row.id):
        if verbose:
            obj['committees'].append(get_committee_by_id(r.committee_id, verbose))
        else:
            obj['committees'].append(r.committee_id)

"""
Get all legislators from the database
"""
def get_legislators(verbose):
    result = []
    for row in session.query(legislator).order_by(legislator.id):
        obj = legislator.get_obj(row)
        add_committee_members(row, obj, verbose)
        add_votes(row, obj, verbose)
        result.append(obj)
    return result

"""
Get all committees from the database
"""
def get_committees(verbose):
    result = []
    for row in session.query(committee).order_by(committee.id):
        obj = committee.get_obj(row)
        result.append(obj)
    return result

"""
Get all bills from the database
"""
def get_bills(verbose):
    result = []
    for row in session.query(bill).order_by(bill.id):
        obj = bill.get_obj(row)
        add_bill_committees(row, obj, verbose)
        result.append(obj)
    return result

"""
Get a legislator by its id from the database
"""
def get_legislator_by_id(legislator_id, verbose):
    row = session.query(legislator).filter(legislator.id == legislator_id).first()
    obj = {}
    if row:
        obj = legislator.get_obj(row)
        add_committee_members(row, obj, verbose)
        add_votes(row, obj, verbose)
    return obj

"""
Get a committee by its id from the database
"""
def get_committee_by_id(committee_id, verbose):
    row = session.query(committee).filter(committee.id == committee_id).first()
    obj = {}
    if row:
        obj = committee.get_obj(row)
    return obj

"""
Get a bill by its id from the database
"""
def get_bill_by_id(bill_id, verbose):
    row = session.query(bill).filter(bill.id == bill_id).first()
    obj = {}
    if row:
        obj = bill.get_obj(row)
        add_bill_committees(row, obj, verbose)
    return obj

