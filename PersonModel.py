import datetime
from SharedModels import db


class PersonModel(db.Model):
    def __init__(self):
        self.time_stamp = datetime.utcnow()

    person_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    email = db.Column(db.Text)
    facebook_id = db.Column(db.Text)
    password = db.Column(db.Text)
    token = db.Column(db.Text)
    time_stamp = db.Column(db.DateTime)

    def to_dict(self):
        json_object = {'personID': self.person_id,
                       'firstName': self.first_name,
                       'lastName': self.last_name,
                       'email': self.email,
                       'facebookID': self.facebook_id,
                       'token': self.token,
                       }

        if not self.time_stamp is None:
            json_object['time_stamp'] = self.time_stamp.isoformat()

        return json_object
