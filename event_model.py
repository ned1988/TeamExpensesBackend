from SharedModels import db


class EventModel(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    creator_event_id = db.Column(db.Integer)
    creation_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    modified_date = db.Column(db.Date)
    sum = db.Column(db.Float)
    title = db.Column(db.Text)

    def to_dict(self):
        json_object = {'eventID': self.event_id,
                       'creatorEventID': self.creator_event_id,
                       'creationDate': self.creation_date,
                       'endDate': self.end_date,
                       'modifiedDate': self.modified_date,
                       'sum': self.sum,
                       'title': self.title,
                       }

        return json_object
