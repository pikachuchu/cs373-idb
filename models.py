from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

#metadata = MetaData()

Base = declarative_base()

"""
Association between reps and committees.
"""
class committee_member(Base):
    __tablename__ = 'committee_members'
    legislator_id = Column(Integer, primary_key=True)
    committee_id = Column(Integer, primary_key=True)

"""
Association between bills and committees.
"""
class bill_committee(Base):
    __tablename__ = 'bill_committees'
    bill_id = Column(Integer, primary_key=True)
    committee_id = Column(Integer, primary_key=True)

"""
Association between legislators and bills
"""
class vote(Base):
    __tablename__ = 'votes'
    legislator_id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, primary_key=True)
    result = Column(String(80))

"""
Model for legislators.
This model is used for both senators and members of the House of Representatives.
There is a many-to-many relationship with committees.
"""
class legislator(Base):
    __tablename__ = 'legislators'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(80))
    last_name = Column(String(80))
    chamber = Column(String(80))
    gender = Column(String(80))
    birthday = Column(String(80))
    party = Column(String(80))
    state = Column(String(80))
    twitter = Column(String(80))
    website = Column(String(80))
    bio_guide = Column(String(80))
    contact_form = Column(String(2048))
    image = Column(String(2048))
    #committees = relationship("committee", secondary=rep_committee_table)

    def get_obj(row):
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

    #search_vector = Column(TSVectorType('first_name', 'last_name', 'chamber', 'party', 'state'))

"""
Model for Congressional committees.
There is a one-to-one relationship with representatives (the committee chair).
"""
class committee(Base):
    __tablename__ = 'committees'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    chamber = Column(String(80))
    website = Column(String(80))
    jurisdiction = Column(Text)
    is_subcommittee = Column(Boolean)
    committee_id = Column(String(80))
    fk_chair = Column(Integer, nullable=True)

    def get_obj(row):
        return {
            'id': row.id,
            'name': row.name,
            'chamber': row.chamber,
            'website': row.website,
            'jurisdiction': row.jurisdiction,
            'is_subcommittee': row.is_subcommittee,
            'committee_id': row.committee_id,
            'chair': row.fk_chair
        }

    #search_vector = Column(TSVectorType('name', 'chamber', 'chair'))

"""
Model for recent bills.
There is a one-to-one relationship with representatives (the sponsor).
There is a many-to-many relationship with committees.
"""
class bill(Base):
    __tablename__ = 'bills'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    bill_id = Column(String(80))
    bill_type = Column(String(80))
    date_intro = Column(String(80))
    house_status = Column(String(80))
    senate_status = Column(String(80))
    link = Column(String(2048))
    current_status_label = Column(Text)
    current_status_description = Column(Text)
    current_status = Column(String(80))
    fk_sponsor = Column(Integer, nullable=True)

    def get_obj(row):
        return {
            'id': row.id,
            'name': row.name,
            'bill_id': row.bill_id,
            'bill_type': row.bill_type,
            'date_intro': row.date_intro,
            'house_status': row.house_status,
            'senate_status': row.senate_status,
            'link': row.link,
            'current_status_label': row.current_status_label,
            'current_status_description': row.current_status_description,
            'current_status': row.current_status,
            'sponsor': row.fk_sponsor
        }
    #search_vector = Column(TSVectorType('name', 'year', 'result'))

if __name__ == "__main__":
    engine = create_engine('mysql+mysqldb://phub:@localhost/phub?charset=utf8')
    Base.metadata.create_all(engine)
