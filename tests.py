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
  
    #Test that the table reps is writable
    def test_write_rep(self):

        query = session.query(legislator).all()
        startSize = len(query)

        session.add(legislator(first_name = "TESTWRITE", party="TEST"))
        session.commit()
        query = session.query(legislator).all()

        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)    

    #Test that the table rep is readable
    def test_read_rep(self):

        session.add(legislator(first_name = "TESTREAD", party="TEST"))
        session.commit()

        query = session.query(legislator).all()
        found = False

        for x in query:
            if(x.first_name == "TESTREAD"):
                found = True

        assert(found)

    def test_read_rep_attribute(self):

        session.add(legislator(last_name = "TESTATTR", party = "Republican"))
        session.commit()

        query = session.query(legislator).filter(legislator.last_name == "TESTATTR").first()

        assert (query is not None)
        assert (query.party == "Republican")
        


     
    #Test deletion of a row in rep
    def test_delete_rep_row(self):
        

        session.add(legislator(last_name = "delete"))
        session.commit()

        query = session.query(legislator).filter(legislator.last_name == "delete").first()

        assert(query != None)

        session.delete(query);
        session.commit()

        toRemove = session.query(legislator).filter(legislator.last_name == "delete").first()
        assert(toRemove == None)

       
    

    def test_write_committee (self):

        query = session.query(committee).all()
        startSize = len(query)

        session.add(committee(name = "TEST"))
        res = session.query(committee).all()
        session.commit()

        query = session.query(committee).all()
        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)    

    #Test that the table committee is readable
    def test_read_committee(self):

        session.add(committee(name = "Ways and Means"))
        session.commit()

        query = session.query(committee).all()
        found = False

        for x in query:
            if(x.name == "Ways and Means"):
                found = True

        assert(found)

    def test_read_committee_attribute(self):

        session.add(committee(name = "AttrTest", chamber = "House"))
        session.commit()

        query = session.query(committee).filter(committee.name == "AttrTest").first()

        assert (query is not None)
        assert (query.chamber == "House")
        
    
    #Test deletion of a row in committee
    def test_delete_committee_row(self):
        

        session.add(committee(name = "delete"))
        session.commit()

        query = session.query(committee).filter(committee.name == "delete").first()

        assert(query != None)

        session.delete(query);
        session.commit()

        toRemove = session.query(committee).filter(committee.name == "delete").first()
        assert(toRemove == None)

    def test_write_committee_member(self):
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

    def test_read_commmittee_member(self):

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
   
    def test_delete_committee_member_row(self):
        session.add(committee_member(legislator_id = 10, committee_id = 10))
        session.commit()

        query = session.query(committee_member).filter(committee_member.legislator_id == 10).first()

        assert(query != None)

        session.delete(query);
        session.commit()

        toRemove = session.query(committee_member).filter(committee_member.legislator_id == 10).first()
        assert(toRemove == None)

    def test_write_bill (self):

        query = session.query(bill).all()
        startSize = len(query)

        session.add(bill(name = "Test"))
        res = session.query(bill).all()
        session.commit()

        query = session.query(bill).all()
        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)    

    #Test that the table bill is readable
    def test_read_bill(self):

        session.add(bill(name = "Test"))
        session.commit()

        query = session.query(bill).all()
        found = False

        for x in query:
            if(x.name == "Test"):
                found = True

        assert(found)

    def test_read_bill_attribute(self):

        session.add(bill(name = "AttrTest", house_status = "Passed"))
        session.commit()

        query = session.query(bill).filter_by(name = "AttrTest").first()
       
        assert (query is not None)
        assert (query.house_status == "Passed")
        
    #Test deletion of a row in bill
    def test_delete_bill_row(self):
        session.add(bill(name = "delete"))
        session.commit()

        query = session.query(bill).filter(bill.name == "delete").first()

        assert(query != None)

        session.delete(query);
        session.commit()

        toRemove = session.query(bill).filter(bill.name == "delete").first()
        assert(toRemove == None)
    
if __name__ == "__main__":
    engine = create_engine('mysql+mysqldb://phub:@localhost/test?charset=utf8')
    Session = sessionmaker(bind=engine)
    session = Session()
    engine.echo = True
    Base.metadata.create_all(engine)
    main()
