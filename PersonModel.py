from SharedModels import db
from data_version_model import DataVersionModel


class PersonModel(db.Model):
    def __init__(self):
        self.data_version = DataVersionModel.data_version()

    person_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    facebook_id = db.Column(db.Text)
    password = db.Column(db.Text)
    token = db.Column(db.Text)
    data_version = db.Column(db.Integer)

    def to_dict(self):
        json_object = {'personID': self.person_id,
                       'firstName': self.first_name,
                       'lastName': self.last_name,
                       'email': self.email,
                       'facebookID': self.facebook_id,
                       'token': self.token,
                       'data_version': self.data_version
                       }

        return json_object
