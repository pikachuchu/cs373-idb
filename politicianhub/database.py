from models import committee_member, bill_committee, vote, legislator, committee, bill

#committee_member, bill_committee, vote, legislator, committee, bill
def add_committee_members(row, obj, verbose):
    obj['committees'] = []
    for r in committee_member.query.filter(committee_member.legislator_id == row.id):
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
    for r in bill_committee.query.filter(bill_committee.bill_id == row.id):
        if verbose:
            obj['committees'].append(get_committee_by_id(r.committee_id, verbose))
        else:
            obj['committees'].append(r.committee_id)
    
"""
Get all legislators from the database
"""
def get_legislators(args, verbose):
    result = []
    query = legislator.query.order_by(legislator.id).filter_by(**args)
    for row in query:
        obj = legislator.get_obj(row)
        add_committee_members(row, obj, verbose)
        add_votes(row, obj, verbose)
        result.append(obj)
    return result

"""
Get all committees from the database
"""
def get_committees(args, verbose):
    result = []
    query = committee.query.order_by(committee.id).filter_by(**args)
    for row in query:
        obj = committee.get_obj(row)
        if verbose:
            obj['chair'] = get_legislator_by_id(obj['chair'], False)
        result.append(obj)
    return result

"""
Get all bills from the database
"""
def get_bills(args, verbose):
    result = []
    query = bill.query.order_by(bill.id).filter_by(**args)
    for row in query:
        obj = bill.get_obj(row)
        add_bill_committees(row, obj, verbose)
        if verbose:
            obj['sponsor'] = get_legislator_by_id(obj['sponsor'], False)
        result.append(obj)
    return result

"""
Get a legislator by its id from the database
"""
def get_legislator_by_id(legislator_id, verbose):
    row = legislator.query.filter(legislator.id == legislator_id).first()
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
    row = committee.query.filter(committee.id == committee_id).first()
    obj = {}
    if row:
        obj = committee.get_obj(row)
        if verbose:
            obj['chair'] = get_legislator_by_id(obj['chair'], False)
    return obj

"""
Get a bill by its id from the database
"""
def get_bill_by_id(bill_id, verbose):
    row = bill.query.filter(bill.id == bill_id).first()
    obj = {}
    if row:
        obj = bill.get_obj(row)
        add_bill_committees(row, obj, verbose)
        if verbose:
            obj['sponsor'] = get_legislator_by_id(obj['sponsor'], False)
    return obj
