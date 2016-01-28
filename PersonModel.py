from sqlalchemy import orm
from datetime import datetime

from SharedModels import db
from constants import Constants


class PersonModel(db.Model):
    __tablename__ = 'person_model'

    k_token = 'token'
    k_email = 'email'
    k_person_id = 'personID'
    k_last_name = 'lastName'
    k_first_name = 'firstName'
    k_facebook_id = 'facebookID'

    person_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    facebook_id = db.Column(db.Text)
    password = db.Column(db.Text)
    token = db.Column(db.Text)
    time_stamp = db.Column(db.DateTime)

    event_owner = db.relationship("EventModel")

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

    @classmethod
    def find_person_by_email(cls, email):
        if email is None:
            return None

        items = PersonModel.query.filter_by(email=email).all()

        if len(items) > 0:
            return items[0]

        return None

    def configure_with_dict(self, dict_model):
        self.email = dict_model.get(self.k_email)
        self.last_name = dict_model.get(self.k_last_name)
        self.first_name = dict_model.get(self.k_first_name)
        self.facebook_id = dict_model.get(self.k_facebook_id)
        self.internal_person_id = dict_model.get(Constants.k_internal_id)

        # Update time stamp value in table
        self.time_stamp = datetime.utcnow()

    def to_dict(self):
        json_object = {self.k_person_id: self.person_id,
                       self.k_first_name: self.first_name,
                       self.k_last_name: self.last_name,
                       self.k_email: self.email,
                       self.k_facebook_id: self.facebook_id,
                       }

        if self.time_stamp is not None:
            json_object[Constants.k_time_stamp] = self.time_stamp.isoformat()

        if self.internal_person_id is not None:
            json_object[Constants.k_internal_id] = self.internal_person_id

        return json_object
