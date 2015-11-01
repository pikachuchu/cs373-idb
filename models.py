from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Table, Text
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

rep_committee_table = Table('rep_committee_assoc', Base.metadata,
    Column('rep_id', Integer, ForeignKey('rep.id')),
    Column('committee_id', Integer, ForeignKey('committee.id'))
)

Association between bills and committees.

bill_committee_table = Table('bill_committee_assoc', Base.metadata,
    Column('bill_id', Integer, ForeignKey('bill.id')),
    Column('committee_id', Integer, ForeignKey('committee.id'))
)


Model for representatives.
This model is used for both senators and members of the House of Representatives.
There is a many-to-many relationship with committees.
"""

class rep(Base):
    __tablename__ = 'rep'
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
    contact_form = Column(String(256))
    image = Column(String(256))
    #committees = relationship("committee", secondary=rep_committee_table)

    #search_vector = Column(TSVectorType('first_name', 'last_name', 'chamber', 'party', 'state'))

"""
Model for Congressional committees.
There is a one-to-one relationship with representatives (the committee chair).
"""
class committee(Base):
    __tablename__ = 'committee'
    id = Column(String(80), primary_key=True)
    name = Column(String(80))
    chamber = Column(String(80))
    website = Column(String(80))
    jurisdiction = Column(Text)
    fk_chair = Column(Integer, ForeignKey("rep.id"))

    #search_vector = Column(TSVectorType('name', 'chamber', 'chair'))

"""
Model for recent bills.
There is a one-to-one relationship with representatives (the sponsor).
There is a many-to-many relationship with committees.
"""
class bill(Base):
    __tablename__ = 'bill'
    id = Column(String(80), primary_key=True)
    name = Column(String(80))
    date_intro = Column(String(80))
    house_status = Column(String(80))
    senate_status = Column(String(80))
    fk_sponsor = Column(Integer, ForeignKey("rep.id"))
    #committees = relationship("committee", secondary=bill_committee_table)

    #search_vector = Column(TSVectorType('name', 'year', 'result'))




if __name__ == "__main__":
    engine = create_engine('mysql+mysqldb://root:politicianhub@localhost/phub')
    Base.metadata.create_all(engine)
