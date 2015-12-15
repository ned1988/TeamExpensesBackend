from SharedModels import db
from datetime import datetime


class EventModel(db.Model):
    def __init__(self):
        self.sum = 0.0
        self.creation_date = datetime.utcnow()
        self.time_stamp = self.creation_date

    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    creator_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    sum = db.Column(db.Float)
    time_stamp = db.Column(db.DateTime)

    @classmethod
    def data_version_difference(self, user_id, data_version):
        items = EventModel.query.filter(EventModel.data_version > data_version).all()

        return {}

    def to_dict(self):
        json_object = {'eventID': self.event_id,
                       'creatorID': self.creator_id,
                       'sum': self.sum,
                       'title': self.title,
                       }

        if not self.creation_date is None:
            json_object['creationDate'] = self.creation_date.isoformat()

        if not self.end_date is None:
            json_object['endDate'] = self.end_date.isoformat()

        if not self.time_stamp is None:
            json_object['timeStamp'] = self.time_stamp.isoformat()

        return json_object
