from SharedModels import db
from datetime import datetime


class EventModel(db.Model):
    def __init__(self):
        self.sum = 0.0
        self.creation_date = datetime.utcnow()
        self.modified_date = self.creation_date

    event_id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)
    sum = db.Column(db.Float)
    title = db.Column(db.Text)

    def to_dict(self):
        json_object = {'eventID': self.event_id,
                       'creatorID': self.creator_id,
                       'creationDate': self.creation_date.isoformat(),
                       'modifiedDate': self.modified_date.isoformat(),
                       'sum': self.sum,
                       'title': self.title,
                       }

        if self.end_date is None:
            json_object['endDate'] = None
        else:
            json_object['endDate'] = self.end_date.isoformat()

        return json_object
