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
    name = Column(String)
    chamber = Column(String)
    gender = Column(String)
    age = Column(Integer)
    party = Column(String)
    state = Column(String)
    twitter_link = Column(String)
    committees = relationship("committee", secondary=rep_committee_table)

    search_vector = Column(TSVectorType('name', 'chamber', 'party', 'state'))
    )

class committee(Base):
    __tablename__ = 'committee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    chamber = Column(String)
    website = Column(String)
    description = Column(Text)
    fk_chair = Column(Integer, ForeignKey("rep.id"))

    search_vector = Column(TSVectorType('name', 'chamber'))
    )

class bill(Base):
    __tablename__ = 'bill'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    result = Column(String)
    fk_committee = Column(Integer, ForeignKey("committee.id"))
    fk_sponsor = Column(Integer, ForeignKey("rep.id"))

    search_vector = Column(TSVectorType('name', 'year', 'result'))
    )

rep_committee_table = Table('association', Base.metadata,
    Column('rep_id', Integer, ForeignKey('rep.id')),
    Column('committee_id', Integer, ForeignKey('committee.id'))
)