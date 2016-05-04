from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()

"""
Association between legislators and committees.
"""
class committee_member(db.Model):
    __tablename__ = 'committee_members'
    legislator_id = db.Column(db.Integer, primary_key=True)
    committee_id = db.Column(db.Integer, primary_key=True)

"""
Association between bills and committees.
"""
class bill_committee(db.Model):
    __tablename__ = 'bill_committees'
    bill_id = db.Column(db.Integer, primary_key=True)
    committee_id = db.Column(db.Integer, primary_key=True)

"""
Association between legislators and bills.
"""
class vote(db.Model):
    __tablename__ = 'votes'
    legislator_id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.String(80))

"""
Model for legislators.
This model is used for both senators and members of the House of Representatives.
There is a many-to-many relationship with committees.
"""
class legislator(db.Model):
    __tablename__ = 'legislators'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    chamber = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    birthday = db.Column(db.String(80))
    party = db.Column(db.String(80))
    state = db.Column(db.String(80))
    twitter = db.Column(db.String(80))
    website = db.Column(db.String(80))
    bio_guide = db.Column(db.String(80))
    contact_form = db.Column(db.String(2048))
    image = db.Column(db.String(2048))

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

"""
Model for Congressional committees.
There is a one-to-one relationship with representatives (the committee chair).
"""
class committee(db.Model):
    __tablename__ = 'committees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    chamber = db.Column(db.String(80))
    website = db.Column(db.String(80))
    jurisdiction = db.Column(db.Text)
    is_subcommittee = db.Column(db.Boolean)
    committee_id = db.Column(db.String(80))
    fk_chair = db.Column(db.Integer, nullable=True)

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

"""
Model for recent bills.
There is a one-to-one relationship with representatives (the sponsor).
There is a many-to-many relationship with committees.
"""
class bill(db.Model):
    __tablename__ = 'bills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    bill_id = db.Column(db.String(80))
    bill_type = db.Column(db.String(80))
    date_intro = db.Column(db.String(80))
    house_status = db.Column(db.String(80))
    senate_status = db.Column(db.String(80))
    link = db.Column(db.String(2048))
    current_status_label = db.Column(db.Text)
    current_status_description = db.Column(db.Text)
    current_status = db.Column(db.String(80))
    fk_sponsor = db.Column(db.Integer, nullable=True)

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

def _create_database():
    from data_loader import populate_db
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print('All tables created')
        populate_db(db.session)

if __name__ == "__main__":
    _create_database()
