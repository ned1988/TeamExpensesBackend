from SharedModels import db

class EventModel(db.Model):
    event_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    creator_event_id = db.Column(db.Integer)
    creation_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    modified_date = db.Column(db.Date)
    status = db.Column(db.Integer)
    summ = db.Column(db.Double)
    sync_state = db.Column(db.Ineger)