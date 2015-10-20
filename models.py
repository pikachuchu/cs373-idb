import os
import sys
 
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
 
 
Base = declarative_base()
make_searchable()
 
 
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
    committees = relationship("committee", secondary=rep_committee_table)

    search_vector = Column(TSVectorType('first_name', 'last_name', 'chamber', 'party', 'state'))
    )

class committee(Base):
    __tablename__ = 'committee'
    id = Column(String, primary_key=True)
    name = Column(String)
    chamber = Column(String)
    website = Column(String)
    phone = Column(String)
    fk_chair = Column(Integer, ForeignKey("rep.id"))

    search_vector = Column(TSVectorType('name', 'chamber', 'chair'))
    )

class bill(Base):
    __tablename__ = 'bill'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_intro = Column(String)
    status = Column(String)
    fk_sponsor = Column(Integer, ForeignKey("rep.id"))
    committees = relationship("committee", secondary=bill_committee_table)

    search_vector = Column(TSVectorType('name', 'year', 'result'))
    )

rep_committee_table = Table('association', Base.metadata,
    Column('rep_id', Integer, ForeignKey('rep.id')),
    Column('committee_id', Integer, ForeignKey('committee.id'))
)

bill_committee_table = Table('association', Base.metadata,
    Column('bill_id', Integer, ForeignKey('bill.id')),
    Column('committee_id', Integer, ForeignKey('committee.id'))
)