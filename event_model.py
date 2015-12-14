from SharedModels import db
from datetime import datetime
from data_version_model import DataVersionModel


class EventModel(db.Model):
    def __init__(self):
        self.sum = 0.0
        self.creation_date = datetime.utcnow()

        version = DataVersionModel()
        self.data_version = version.data_version()
        print self.data_version

    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    creator_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    sum = db.Column(db.Float)
    data_version = db.Column(db.Integer)


    @classmethod
    def data_version_difference(self, user_id, data_version):
        items = EventModel.query.filter(EventModel.data_version > data_version).all()

        return items

    def to_dict(self):
        json_object = {'eventID': self.event_id,
                       'creatorID': self.creator_id,
                       'sum': self.sum,
                       'title': self.title,
                       'data_version': self.data_version
                       }

        if self.creation_date is None:
            json_object['creationDate'] = None
        else:
            json_object['creationDate'] = self.creation_date.isoformat()

        if self.end_date is None:
            json_object['endDate'] = None
        else:
            json_object['endDate'] = self.end_date.isoformat()

        return json_object
