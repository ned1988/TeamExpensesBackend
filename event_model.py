from datetime import datetime
from dateutil.parser import parse
from sqlalchemy.orm import relationship

from SharedModels import db
from expense_model import ExpenseModel
from expense_model import k_expense_id

k_title = 'title'
k_event_id = 'eventID'
k_internal_event_id = 'internalEventID'


class EventModel(db.Model):
    __tablename__ = 'event_model'

    def __init__(self):
        self.is_removed = False
        self.time_stamp = datetime.utcnow()

    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    creator_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    time_stamp = db.Column(db.DateTime)
    is_removed = db.Column(db.Boolean)

    @classmethod
    def time_stamp_difference(cls, user_id, time_stamp):
        if time_stamp is None:
            items = EventModel.query.filter_by(creator_id=user_id).all()
        else:
            items = EventModel.query.filter(EventModel.creator_id == user_id,
                                            EventModel.time_stamp > time_stamp).all()

        return items

    @classmethod
    def find_event(cls, event_id):
        items = EventModel.query.filter_by(event_id=event_id).all()

        if len(items) > 0:
            return items[0]

        return None

    def configure_with_dict(self, dict_model):
        value = dict_model.get(k_title)
        if value is not None:
            self.title = value

        value = dict_model.get('creationDate')
        if value is not None:
            self.creation_date = parse(value)

        value = dict_model.get('timeStamp')
        if value is not None:
            self.time_stamp = parse(value)

        value = dict_model.get('expenses')
        if value is not None and isinstance(value, list):
            result = list(self.expenses)
            for expense_dict in value:
                expense_id = expense_dict.get(k_expense_id)

                expense = ExpenseModel.find_expense(expense_id)
                expense.configure_with_dict(expense_dict)

                result.append(expense)

            self.expenses = result


    def to_dict(self):
        json_object = dict()

        json_object['title'] = self.title
        json_object[k_event_id] = self.event_id
        json_object['creatorID'] = self.creator_id
        json_object['isRemoved'] = self.is_removed

        if self.creation_date is not None:
            json_object['creationDate'] = self.creation_date.isoformat()

        if self.end_date is not None:
            json_object['endDate'] = self.end_date.isoformat()

        if self.time_stamp is not None:
            json_object['timeStamp'] = self.time_stamp.isoformat()

        return json_object

EventModel.expenses = relationship("ExpenseModel", order_by=ExpenseModel.expense_id, back_populates="event_model")