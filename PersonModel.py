from sqlalchemy import orm
from datetime import datetime

from SharedModels import db
from constants import Constants

k_token = 'token'
k_email = 'email'
k_person_id = 'personID'
k_last_name = 'lastName'
k_first_name = 'firstName'
k_facebook_id = 'facebookID'


class PersonModel(db.Model):
    __tablename__ = 'person_model'

    person_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    facebook_id = db.Column(db.Text)
    password = db.Column(db.Text)
    token = db.Column(db.Text)
    time_stamp = db.Column(db.DateTime)

    event_owner = db.relationship("EventModel")

    def __init__(self):
        self.time_stamp = datetime.utcnow()

    @orm.reconstructor
    def init_on_load(self):
        self.internal_person_id = None

    @classmethod
    def find_person(cls, person_id):
        if person_id is None:
            return PersonModel()

        items = PersonModel.query.filter_by(person_id=person_id).all()

        if len(items) > 0:
            return items[0]

        return PersonModel()

    def configure_with_dict(self, dict_model):
        self.email = dict_model.get(k_email)
        self.last_name = dict_model.get(k_last_name)
        self.first_name = dict_model.get(k_first_name)
        self.facebook_id = dict_model.get(k_facebook_id)

    def to_dict(self):
        json_object = {k_person_id: self.person_id,
                       k_first_name: self.first_name,
                       k_last_name: self.last_name,
                       k_email: self.email,
                       k_facebook_id: self.facebook_id,
                       }

        if not self.time_stamp is None:
            json_object[Constants.k_time_stamp] = self.time_stamp.isoformat()

        return json_object
