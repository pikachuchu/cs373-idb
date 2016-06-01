import unittest
from politicianhub.models import *
from flask.ext.testing import TestCase

class Tests(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://travis:@localhost/test'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Test that the table legislators is writable
    def test_write_legislator(self):
        person = legislator(first_name = "TESTWRITE", party="TEST")
        db.session.add(person)
        db.session.commit()
        assert(person in db.session)

    # Test that the table legislators can be written multiple queries
    def test_write_legislator_multiple(self):
        person1 = legislator(first_name = "TESTMULTIPLE1", party="TEST")
        person2 = legislator(first_name = "TESTMULTIPLE2", party="TEST")
        db.session.add(person1)
        db.session.add(person2)
        db.session.commit()

        assert(person1 in db.session)
        assert(person2 in db.session)

    # Test that the table legislators is readable and case insensitive
    def test_read_legislator(self):
        db.session.add(legislator(first_name = "TESTREAD", party="TEST"))
        db.session.commit()

        # query returns None if not found
        query1 = legislator.query.filter_by(first_name = "TESTREAD").first()
        query2 = legislator.query.filter_by(first_name = "testread").first()
        assert(query1 is not None)
        assert(query2 is not None)

    # Test filtering by an attribute
    def test_read_legislator_attribute(self):
        db.session.add(legislator(last_name = "TESTATTR", party = "Republican"))
        db.session.commit()

        query = legislator.query.filter_by(last_name = "TESTATTR").first()

        assert (query is not None)
        assert (query.party == "Republican")

    # Test filtering by an attribute returns multiple unique results
    def test_read_legislator_attribute_multiple(self):
        db.session.add(legislator(last_name = "TESTATTR1", party = "Republican"))
        db.session.add(legislator(last_name = "TESTATTR1", party = "Democrat"))
        db.session.commit()

        queries = legislator.query.filter_by(last_name = "TESTATTR1").all()

        assert (queries is not None)
        assert (len(queries) == 2)

        party = [];
        for x in queries:
            party.append(x.party)

        assert (party[0] != party[1])

    # Test deletion of a row in legislators
    def test_delete_legislators_row(self):
        db.session.add(legislator(last_name = "delete"))
        db.session.commit()

        query = legislator.query.filter_by(last_name = "delete").first()

        assert(query is not None)

        db.session.delete(query);
        db.session.commit()

        toRemove = legislator.query.filter_by(last_name = "delete").first()
        assert(toRemove is None)

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
        test_committee = committee(name = "TEST")
        db.session.add(test_committee)
        db.session.commit()
        assert(test_committee in db.session)

    # Test that the table committees is readable
    def test_read_committees(self):
        db.session.add(committee(name = "Ways and Means"))
        db.session.commit()

        query = committee.query.all()
        found = False

        for x in query:
            if x.name == "Ways and Means":
                found = True

        assert(found)

    # Test filtering an attribute in committees
    def test_read_committee_attribute(self):
        db.session.add(committee(name = "AttrTest", chamber = "House"))
        db.session.commit()

        query = committee.query.filter_by(name = "AttrTest").first()

        assert (query is not None)
        assert (query.chamber == "House")

    # Test deletion of a row in committees
    def test_delete_committee_row(self):
        db.session.add(committee(name = "delete"))
        db.session.commit()

        query = committee.query.filter_by(name = "delete").first()

        assert(query is not None)

        db.session.delete(query);
        db.session.commit()

        toRemove = committee.query.filter_by(name = "delete").first()
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
        query = db.session.query(vote).all()
        startSize = len(query)

        db.session.add(vote(legislator_id = 1, bill_id = 2))
        res = db.session.query(vote).all()
        endSize = len(res)

        self.assertEqual(startSize + 1, endSize)
        query = db.session.query(vote).filter(vote.legislator_id == 1).first()
        db.session.delete(query)

    # Test that the table votes is readable
    def test_read_votes(self):
        db.session.add(vote(legislator_id = 3, bill_id = 4))
        db.session.commit()

        query = db.session.query(vote).all()
        found = False

        for x in query:
            if(x.legislator_id == 3):
                found = True

        assert(found)
        query = db.session.query(vote).filter(vote.legislator_id == 3).first()
        db.session.delete(query)
 
    # Test delete row for the table votes
    def test_delete_votes_row(self):
        db.session.add(vote(legislator_id = 5, bill_id = 6))
        db.session.commit()

        query = db.session.query(vote).filter(vote.legislator_id == 5).first()

        assert(query != None)

        db.session.delete(query);
        db.session.commit()

        toRemove = db.session.query(vote).filter(vote.legislator_id == 5).first()
        assert(toRemove == None)

    # Test that the table bill_committees is writable
    def test_write_bill_committees(self):
        query = db.session.query(bill_committee).all()
        startSize = len(query)

        db.session.add(bill_committee(bill_id = 7, committee_id = 5))
        res = db.session.query(bill_committee).all()
        endSize = len(res)

        self.assertEqual(startSize + 1, endSize)
        query = db.session.query(bill_committee).filter(bill_committee.bill_id == 7).first()
        db.session.delete(query)

    # Test that the table committee_members is readable
    def test_read_bill_committees(self):
        db.session.add(bill_committee(bill_id = 8, committee_id = 9))
        db.session.commit()

        query = db.session.query(bill_committee).all()
        found = False

        for x in query:
            if(x.bill_id == 8):
                found = True

        assert(found)
        query = db.session.query(bill_committee).filter(bill_committee.bill_id == 8).first()
        db.session.delete(query)
 
    # Test delete row for the table bill_committees
    def test_delete_bill_committees_row(self):
        db.session.add(bill_committee(bill_id = 9, committee_id = 10))
        db.session.commit()

        query = db.session.query(bill_committee).filter(bill_committee.bill_id == 9).first()

        assert(query != None)

        db.session.delete(query);
        db.session.commit()

        toRemove = db.session.query(bill_committee).filter(bill_committee.bill_id == 9).first()
        assert(toRemove == None)

    # Test that the table committee_members is writable
    def test_write_committee_members(self):
        query = db.session.query(committee_member).all()
        startSize = len(query)

        db.session.add(committee_member(legislator_id = 8, committee_id = 8))
        res = db.session.query(committee_member).all()
        db.session.commit()

        query = db.session.query(committee_member).all()
        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)
        query = db.session.query(committee_member).filter(committee_member.legislator_id == 8).first()
        db.session.delete(query)

    # Test that the table committee_members is readable
    def test_read_commmittee_members(self):

        db.session.add(committee_member(legislator_id = 9, committee_id = 9))
        db.session.commit()

        query = db.session.query(committee_member).all()
        found = False

        for x in query:
            if(x.legislator_id == 9):
                found = True

        assert(found)
        query = db.session.query(committee_member).filter(committee_member.legislator_id == 9).first()
        db.session.delete(query)
   
    # Test delete row for the table committee_members
    def test_delete_committee_members_row(self):
        db.session.add(committee_member(legislator_id = 10, committee_id = 10))
        db.session.commit()

        query = db.session.query(committee_member).filter(committee_member.legislator_id == 10).first()

        assert(query != None)

        db.session.delete(query);
        db.session.commit()

        toRemove = db.session.query(committee_member).filter(committee_member.legislator_id == 10).first()
        assert(toRemove == None)

    # Test that the table bills is writable
    def test_write_bills(self):

        query = db.session.query(bill).all()
        startSize = len(query)

        db.session.add(bill(name = "Test"))
        res = db.session.query(bill).all()
        db.session.commit()

        query = db.session.query(bill).all()
        endSize = len(query)

        self.assertEqual(startSize + 1, endSize)    

    # Test that the table bills is readable
    def test_read_bill(self):

        db.session.add(bill(name = "Test"))
        db.session.commit()

        query = db.session.query(bill).all()
        found = False

        for x in query:
            if(x.name == "Test"):
                found = True

        assert(found)

    def test_read_bill2(self):

        db.session.add(bill(name = "Test2"))
        db.session.commit()

        query = db.session.query(bill).all()
        found = False

        for x in query:
            if(x.name == "Test2"):
                found = True

        assert(found)

    # Test filtering on an attribute in the table bills
    def test_read_bill_attribute(self):

        db.session.add(bill(name = "AttrTest", house_status = "Passed"))
        db.session.commit()

        query = db.session.query(bill).filter_by(name = "AttrTest").first()
       
        assert (query is not None)
        assert (query.house_status == "Passed")

    def test_read_bill_attribute2(self):

        db.session.add(bill(name = "AttrTest2", house_status = "Failed"))
        db.session.commit()

        query = db.session.query(bill).filter_by(name = "AttrTest2").first()
       
        assert (query is not None)
        assert (query.house_status == "Failed")
        
    # Test deletion of a row in bills
    def test_delete_bill_row(self):
        db.session.add(bill(name = "delete"))
        db.session.commit()

        query = db.session.query(bill).filter(bill.name == "delete").first()

        assert(query != None)

        db.session.delete(query);
        db.session.commit()

        toRemove = db.session.query(bill).filter(bill.name == "delete").first()
        assert(toRemove == None)

    # Test deletion of a row in bills
    def test_delete_bill_row2(self):
        db.session.add(bill(name = "delete2"))
        db.session.commit()

        query = db.session.query(bill).filter(bill.name == "delete2").first()

        assert(query != None)

        db.session.delete(query);
        db.session.commit()

        toRemove = db.session.query(bill).filter(bill.name == "delete2").first()
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
    unittest.main()
