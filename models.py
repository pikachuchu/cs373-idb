from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Table, Text
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_searchable import make_searchable

Base = declarative_base()
make_searchable()

"""
Association between reps and committees.
"""
rep_committee_table = Table('rep_committee_assoc', Base.metadata,
    Column('rep_id', Integer, ForeignKey('rep.id')),
    Column('committee_id', Integer, ForeignKey('committee.id'))
)

"""
Association between bills and committees.
"""
bill_committee_table = Table('bill_committee_assoc', Base.metadata,
    Column('bill_id', Integer, ForeignKey('bill.id')),
    Column('committee_id', Integer, ForeignKey('committee.id'))
)

"""
Model for representatives.
This model is used for both senators and members of the House of Representatives.
There is a many-to-many relationship with committees.
"""
class rep(Base):
    __tablename__ = 'rep'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    chamber = Column(String)
    gender = Column(String)
    birthday = Column(String)
    party = Column(String)
    state = Column(String)
    twitter = Column(String)
    youtube = Column(String)
    website = Column(String)
    contact_form = Column(String)
    image = Column(String)
    committees = relationship("committee", secondary=rep_committee_table)

    search_vector = Column(TSVectorType('first_name', 'last_name', 'chamber', 'party', 'state'))

"""
Model for Congressional committees.
There is a one-to-one relationship with representatives (the committee chair).
"""
class committee(Base):
    __tablename__ = 'committee'
    id = Column(String, primary_key=True)
    name = Column(String)
    chamber = Column(String)
    website = Column(String)
    jurisdiction = Column(Text)
    fk_chair = Column(Integer, ForeignKey("rep.id"))

    search_vector = Column(TSVectorType('name', 'chamber', 'chair'))

"""
Model for recent bills.
There is a one-to-one relationship with representatives (the sponsor).
There is a many-to-many relationship with committees.
"""
class bill(Base):
    __tablename__ = 'bill'
    id = Column(String, primary_key=True)
    name = Column(String)
    date_intro = Column(String)
    house_status = Column(String)
    senate_status = Column(String)
    fk_sponsor = Column(Integer, ForeignKey("rep.id"))
    committees = relationship("committee", secondary=bill_committee_table)

    search_vector = Column(TSVectorType('name', 'year', 'result'))
