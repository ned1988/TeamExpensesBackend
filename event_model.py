from SharedModels import db
from datetime import datetime


class EventModel(db.Model):
    def __init__(self):
        self.sum = 0.0
        self.creation_date = datetime.utcnow()
        self.time_stamp = self.creation_date

    event_id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    time_stamp = db.Column(db.DateTime)
    sum = db.Column(db.Float)
    title = db.Column(db.Text)

    @classmethod
    def time_stamp_difference(self, user_id, time_stamp):
        items = EventModel.query.filter(EventModel.time_stamp > time_stamp).all()

        return items

    def to_dict(self):
        json_object = {'eventID': self.event_id,
                       'creatorID': self.creator_id,
                       'sum': self.sum,
                       'title': self.title,
                       }

        if self.creation_date is None:
            json_object['creationDate'] = None
        else:
            json_object['creationDate'] = self.creation_date.isoformat()

        if self.end_date is None:
            json_object['endDate'] = None
        else:
            json_object['endDate'] = self.end_date.isoformat()

        if self.time_stamp is None:
            json_object['time_stamp'] = None
        else:
            json_object['time_stamp'] = self.time_stamp.isoformat()

        return json_object
