import datetime

from SharedModels import db
from constants import Constants

k_token = 'token'
k_personID = 'personID'


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

    def to_dict(self):
        json_object = {k_personID: self.person_id,
                       'firstName': self.first_name,
                       'lastName': self.last_name,
                       'email': self.email,
                       'facebookID': self.facebook_id,
                       }

        if not self.time_stamp is None:
            json_object[Constants.k_time_stamp] = self.time_stamp.isoformat()

        return json_object
