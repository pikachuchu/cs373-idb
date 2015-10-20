from unittest import main, TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from sqlalchemy_searchable import search

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float, LargeBinary, Boolean

import threading
from flask import Flask, render_template, url_for, g, request, session, redirect, abort, flash
from flask.ext.sqlalchemy import SQLAlchemy

from models import *
from __init__ import unittests
unittests()

#for this tests to work you need to have a postgres database 
#set up with the name testdb, no username, no password

class tests(TestCase):

    #setup the database
    def setUp(self):
        db.configure_mappers()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    
    #Test that the table reps is writable
    def test_write_rep(self):

        query = rep.query.all()
        startSize = len(query)

        db.session.add(rep(name = "TESTWRITE", party="TEST"))
        db.session.commit()
        query = rep.query.all()

        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)    

    #Test that the table rep is readable
    def test_read_rep(self):

        db.session.add(rep(name = "TESTREAD", party="TEST"))
        db.session.commit()

        query = rep.query.all()
        found = False

        for x in query:
            if(x.name == "TESTREAD"):
                found = True

        assert(found)

    def test_read_rep_attribute(self):

        db.session.add(rep(name = "TESTATTR", party = "Republican"))
        db.session.commit()

        query = db.session.query(rep).filter(rep.name == "TESTATTR").first()

        assert (query is not None)
        assert (query.description == "Republican")
        


     
    #Test deletion of a row in rep
    def test_delete_rep_row(self):
        

        db.session.add(rep(name = "delete"))
        db.session.commit()

        query = db.session.query(rep).filter(rep.name == "delete").first()

        assert(query != None)

        db.session.delete(query);
        db.session.commit()

        toRemove = db.session.query(rep).filter(rep.name == "delete").first()
        assert(toRemove == None)

       
    

    def test_write_committee (self):

        query = db.session.query(committee).all()
        startSize = len(query)

        db.session.add(committee(name = "TEST"))
        res = db.session.query(committee).all()
        db.session.commit()

        query = db.session.query(committee).all()
        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)    

        #Test that the table committee is readable
    def test_read_committee(self):

        db.session.add(committee(name = "Ways and Means"))
        db.session.commit()

        query = db.session.query(committee).all()
        found = False

        for x in query:
            if(x.name == "Ways and Means"):
                found = True

        assert(found)

    def test_read_committee_attribute(self):

        db.session.add(committee(name = "Ways and Means", description = "Budget"))
        db.session.commit()

        query = db.session.query(committee).filter(committee.name == "Ways and Means").first()

        assert (query is not None)
        assert (query.description == "Budget")
        
    
    #Test deletion of a row in committee
    def test_delete_committee_row(self):
        

        db.session.add(committee(name = "delete"))
        db.session.commit()

        query = db.session.query(committee).filter(committee.name == "delete").first()

        assert(query != None)

        db.session.delete(query);
        db.session.commit()

        toRemove = db.session.query(committee).filter(committee.name == "delete").first()
        assert(toRemove == None)

        

   
    def test_write_bill (self):

        query = db.session.query(bill).all()
        startSize = len(query)

        db.session.add(bill(name = "Test"))
        res = db.session.query(bill).all()
        db.session.commit()

        query = db.session.query(bill).all()
        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)    

        #Test that the table bill is readable
    def test_read_bill(self):

        db.session.add(bill(name = "Test"))
        db.session.commit()

        query = db.session.query(bill).all()
        found = False

        for x in query:
            if(x.name == "Test"):
                found = True

        assert(found)

    def test_read_bill_attribute(self):

        db.session.add(bill(name = "Test", result = "Passed"))
        db.session.commit()

        query = db.session.query(bill).filter_by(name = "Test").first()
       
        assert (query is not None)
        assert (query.result == "Passed")
        

    
    #Test deletion of a row in bill
    def test_delete_bill_row(self):
        db.session.add(bill(name = "delete"))
        db.session.commit()

        query = db.session.query(bill).filter(bill.name == "delete").first()

        assert(query != None)

        db.session.delete(query);
        db.session.commit()

        toRemove = db.session.query(bill).filter(bill.name == "delete").first()
        assert(toRemove == None)
    
    


    
if __name__ == "__main__":
    main()