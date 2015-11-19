from unittest import main, TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 

from flask import *
from flask import request
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float, LargeBinary, Boolean

import threading
from flask import Flask, render_template, url_for, g, request, session, redirect, abort, flash

from models import *

class tests(TestCase):
  
    # Test that the table legislators is writable
    def test_write_legislator(self):

        query = session.query(legislator).all()
        startSize = len(query)

        session.add(legislator(first_name = "TESTWRITE", party="TEST"))
        session.commit()
        query = session.query(legislator).all()

        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)  

    # Test that the table legislators can be written multiple queries 
    def test_write_legislator_multiple(self):

        query = session.query(legislator).all()
        startSize = len(query)

        session.add(legislator(first_name = "TESTMULTIPLE", party="TEST"))
        session.add(legislator(first_name = "TESTMULTIPLE", party="TEST"))
        session.commit()
        query = session.query(legislator).all()

        endSize = len(query)

        self.assertEqual(startSize + 2, endSize)    

    # Test that the table legislators is writable
    def test_write_legislator_1(self):

        query = session.query(legislator).all()
        startSize = len(query)

        session.add(legislator(first_name = "OTHERWRITE", party="TEST"))
        session.commit()
        query = session.query(legislator).all()

        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)    

    # Test that the table legislators is writable
    def test_write_legislator_2(self):

        query = session.query(legislator).all()
        startSize = len(query)

        session.add(legislator(first_name = "WRITETWO", party="TEST"))
        session.commit()
        query = session.query(legislator).all()

        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)    

    # Test that the table legislators is writable
    def test_write_legislator_3(self):

        query = session.query(legislator).all()
        startSize = len(query)

        session.add(legislator(first_name = "WRITETHREE", party="TEST"))
        session.commit()
        query = session.query(legislator).all()

        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)    

    # Test that the table legislators is readable
    def test_read_legislator(self):

        session.add(legislator(first_name = "TESTREAD", party="TEST"))
        session.commit()

        query = session.query(legislator).all()
        found = False

        for x in query:
            if(x.first_name == "TESTREAD"):
                found = True

        assert(found)

    # Test that the table legislators is readable and for case sensitivity
    def test_read_legislator_sensitivity(self):

        session.add(legislator(first_name = "TESTREAD2", party="TEST2"))
        session.commit()

        query = session.query(legislator).all()
        found = False

        for x in query:
            if(x.first_name == "TESTREAD2"):
                found = True
            if(x.first_name == "testread2"):
                found = False

        assert(found)

    # Test filtering by an attribute
    def test_read_legislator_attribute(self):

        session.add(legislator(last_name = "TESTATTR", party = "Republican"))
        session.commit()

        query = session.query(legislator).filter(legislator.last_name == "TESTATTR").first()

        assert (query is not None)
        assert (query.party == "Republican")

    # Test filtering by an attribute returns multiple unique results
    def test_read_legislator_attribute_multiple(self):

        session.add(legislator(last_name = "TESTATTR1", party = "Republican"))
        session.add(legislator(last_name = "TESTATTR1", party = "Democrat"))
        session.commit()

        queries = session.query(legislator).filter(legislator.last_name == "TESTATTR1").all()

        assert (queries is not None)
        assert (len(queries) == 2)

        party = [];
        for x in queries :
            party.append(x.party)

        assert (party[0] != party[1])
     
    # Test deletion of a row in legislators
    def test_delete_legislators_row(self):
        
        session.add(legislator(last_name = "delete"))
        session.commit()

        query = session.query(legislator).filter(legislator.last_name == "delete").first()

        assert(query != None)

        session.delete(query);
        session.commit()

        toRemove = session.query(legislator).filter(legislator.last_name == "delete").first()
        assert(toRemove == None)

    def test_legislator_get_obj(self):
        row = legislator(
            id=1,
            first_name='first',
            last_name='last',
            chamber='house',
            gender='male',
            birthday='2015-11-05',
            party='R',
            state='TX',
            twitter='twitter',
            website='website',
            bio_guide='123456',
            contact_form='form',
            image='image',
        )
        result = {
            'id': 1,
            'first_name': 'first',
            'last_name': 'last',
            'chamber': 'house',
            'gender': 'male',
            'birthday': '2015-11-05',
            'party': 'R',
            'state': 'TX',
            'twitter': 'twitter',
            'website': 'website',
            'bio_guide': '123456',
            'contact_form': 'form',
            'image': 'image'
        }

        assert(legislator.get_obj(row) == result)

    # Test that the table committees is writable
    def test_write_committees(self):

        query = session.query(committee).all()
        startSize = len(query)

        session.add(committee(name = "TEST"))
        res = session.query(committee).all()
        session.commit()

        query = session.query(committee).all()
        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)    

    # Test that the table committees is readable
    def test_read_committees(self):

        session.add(committee(name = "Ways and Means"))
        session.commit()

        query = session.query(committee).all()
        found = False

        for x in query:
            if(x.name == "Ways and Means"):
                found = True

        assert(found)

    # Test filtering an attribute in committees
    def test_read_committee_attribute(self):

        session.add(committee(name = "AttrTest", chamber = "House"))
        session.commit()

        query = session.query(committee).filter(committee.name == "AttrTest").first()

        assert (query is not None)
        assert (query.chamber == "House")
        
    # Test deletion of a row in committees
    def test_delete_committee_row(self):

        session.add(committee(name = "delete"))
        session.commit()

        query = session.query(committee).filter(committee.name == "delete").first()

        assert(query != None)

        session.delete(query);
        session.commit()

        toRemove = session.query(committee).filter(committee.name == "delete").first()
        assert(toRemove == None)

    def test_committee_get_obj(self):
        row = committee(
            id=2,
            name='committee_name',
            chamber='senate',
            website='website',
            jurisdiction='hi',
            is_subcommittee='true',
            committee_id='123',
            fk_chair=5
        )
        result = {
            'id': 2,
            'name': 'committee_name',
            'chamber': 'senate',
            'website': 'website',
            'jurisdiction': 'hi',
            'is_subcommittee': 'true',
            'committee_id': '123',
            'chair': 5
        }
        assert(committee.get_obj(row) == result)

    # Test that the table votes is writable
    def test_write_votes(self):
        query = session.query(vote).all()
        startSize = len(query)

        session.add(vote(legislator_id = 1, bill_id = 2))
        res = session.query(vote).all()
        endSize = len(res)

        self.assertEqual(startSize + 1, endSize)
        query = session.query(vote).filter(vote.legislator_id == 1).first()
        session.delete(query)

    # Test that the table votes is readable
    def test_read_votes(self):
        session.add(vote(legislator_id = 3, bill_id = 4))
        session.commit()

        query = session.query(vote).all()
        found = False

        for x in query:
            if(x.legislator_id == 3):
                found = True

        assert(found)
        query = session.query(vote).filter(vote.legislator_id == 3).first()
        session.delete(query)
 
    # Test delete row for the table votes
    def test_delete_votes_row(self):
        session.add(vote(legislator_id = 5, bill_id = 6))
        session.commit()

        query = session.query(vote).filter(vote.legislator_id == 5).first()

        assert(query != None)

        session.delete(query);
        session.commit()

        toRemove = session.query(vote).filter(vote.legislator_id == 5).first()
        assert(toRemove == None)

    # Test that the table bill_committees is writable
    def test_write_bill_committees(self):
        query = session.query(bill_committee).all()
        startSize = len(query)

        session.add(bill_committee(bill_id = 7, committee_id = 5))
        res = session.query(bill_committee).all()
        endSize = len(res)

        self.assertEqual(startSize + 1, endSize)
        query = session.query(bill_committee).filter(bill_committee.bill_id == 7).first()
        session.delete(query)

    # Test that the table committee_members is readable
    def test_read_bill_committees(self):
        session.add(bill_committee(bill_id = 8, committee_id = 9))
        session.commit()

        query = session.query(bill_committee).all()
        found = False

        for x in query:
            if(x.bill_id == 8):
                found = True

        assert(found)
        query = session.query(bill_committee).filter(bill_committee.bill_id == 8).first()
        session.delete(query)
 
    # Test delete row for the table bill_committees
    def test_delete_bill_committees_row(self):
        session.add(bill_committee(bill_id = 9, committee_id = 10))
        session.commit()

        query = session.query(bill_committee).filter(bill_committee.bill_id == 9).first()

        assert(query != None)

        session.delete(query);
        session.commit()

        toRemove = session.query(bill_committee).filter(bill_committee.bill_id == 9).first()
        assert(toRemove == None)

    # Test that the table committee_members is writable
    def test_write_committee_members(self):
        query = session.query(committee_member).all()
        startSize = len(query)

        session.add(committee_member(legislator_id = 8, committee_id = 8))
        res = session.query(committee_member).all()
        session.commit()

        query = session.query(committee_member).all()
        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)
        query = session.query(committee_member).filter(committee_member.legislator_id == 8).first()
        session.delete(query)

    # Test that the table committee_members is readable
    def test_read_commmittee_members(self):

        session.add(committee_member(legislator_id = 9, committee_id = 9))
        session.commit()

        query = session.query(committee_member).all()
        found = False

        for x in query:
            if(x.legislator_id == 9):
                found = True

        assert(found)
        query = session.query(committee_member).filter(committee_member.legislator_id == 9).first()
        session.delete(query)
   
    # Test delete row for the table committee_members
    def test_delete_committee_members_row(self):
        session.add(committee_member(legislator_id = 10, committee_id = 10))
        session.commit()

        query = session.query(committee_member).filter(committee_member.legislator_id == 10).first()

        assert(query != None)

        session.delete(query);
        session.commit()

        toRemove = session.query(committee_member).filter(committee_member.legislator_id == 10).first()
        assert(toRemove == None)

    # Test that the table bills is writable
    def test_write_bills(self):

        query = session.query(bill).all()
        startSize = len(query)

        session.add(bill(name = "Test"))
        res = session.query(bill).all()
        session.commit()

        query = session.query(bill).all()
        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)    

    # Test that the table bills is readable
    def test_read_bill(self):

        session.add(bill(name = "Test"))
        session.commit()

        query = session.query(bill).all()
        found = False

        for x in query:
            if(x.name == "Test"):
                found = True

        assert(found)

    # Test filtering on an attribute in the table bills
    def test_read_bill_attribute(self):

        session.add(bill(name = "AttrTest", house_status = "Passed"))
        session.commit()

        query = session.query(bill).filter_by(name = "AttrTest").first()
       
        assert (query is not None)
        assert (query.house_status == "Passed")
        
    # Test deletion of a row in bills
    def test_delete_bill_row(self):
        session.add(bill(name = "delete"))
        session.commit()

        query = session.query(bill).filter(bill.name == "delete").first()

        assert(query != None)

        session.delete(query);
        session.commit()

        toRemove = session.query(bill).filter(bill.name == "delete").first()
        assert(toRemove == None)

    def test_bill_get_obj(self):
      
        row = bill(
            id=3,
            name='bill',
            bill_id='12345',
            bill_type='house_bill',
            date_intro='2015-11-04',
            house_status='pass',
            senate_status='fail',
            link='link',
            current_status_label='label',
            current_status_description='description',
            current_status='status',
            fk_sponsor=4
        )
        result = {
            'id': 3,
            'name': 'bill',
            'bill_id': '12345',
            'bill_type': 'house_bill',
            'date_intro': '2015-11-04',
            'house_status': 'pass',
            'senate_status': 'fail',
            'link': 'link',
            'current_status_label': 'label',
            'current_status_description': 'description',
            'current_status': 'status',
            'sponsor': 4
        }
        assert(bill.get_obj(row) == result)
    
if __name__ == "__main__":
    engine = create_engine('mysql+mysqldb://travis:@localhost/test?charset=utf8')
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    main()
