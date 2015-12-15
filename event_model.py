import datetime
from SharedModels import db


class EventModel(db.Model):
    def __init__(self):
        self.sum = 0.0
        self.is_removed = False
        self.creation_date = datetime.utcnow()
        self.time_stamp = self.creation_date

    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    creator_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    sum = db.Column(db.Float)
    time_stamp = db.Column(db.DateTime)
    is_removed = db.Column(db.Boolean)

    @classmethod
    def time_stamp_difference(self, user_id, time_stamp):
        items = EventModel.query.filter(EventModel.creator_id == user_id,
                                        EventModel.time_stamp > time_stamp).all()

        return [model.to_dict() for model in items]

    def to_dict(self):
        json_object = {'sum': self.sum}

        json_object['title'] = self.title
        json_object['eventID'] = self.event_id
        json_object['creatorID'] = self.creator_id
        json_object['is_removed'] = self.is_removed

        if self.creation_date is not None:
            json_object['creationDate'] = self.creation_date.isoformat()

        if self.end_date is not None:
            json_object['endDate'] = self.end_date.isoformat()

        if self.time_stamp is not None:
            json_object['timeStamp'] = self.time_stamp.isoformat()

        return json_object
