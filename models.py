from sqlalchemy_utils.types import TSVectorType
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_searchable import make_searchable
from sqlalchemy import *

#metadata = MetaData()

Base = declarative_base()
make_searchable()

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
#committees = relationship("committee", secondary=bill_committee_table)

    #search_vector = Column(TSVectorType('name', 'year', 'result'))

if __name__ == "__main__":
    engine = create_engine('mysql+mysqldb://root:politicianhub@localhost/phub?charset=utf8')
    Base.metadata.create_all(engine)
