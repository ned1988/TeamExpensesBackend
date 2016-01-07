from datetime import datetime
from dateutil.parser import parse
from sqlalchemy.orm import relationship

from SharedModels import db

k_title = 'title'
k_is_removed = 'isRemoved'
k_time_stamp = 'timeStamp'
k_expense_id = 'expense_id'
k_creation_date = 'creationDate'
k_internal_expense_id = 'internalID'


class ExpenseModel(db.Model):
    __tablename__ = 'expense_model'

    expense_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)
    creation_date = db.Column(db.DateTime)
    event_id = db.Column(db.Integer, db.ForeignKey('event_model.event_id'))

    event_model = relationship("EventModel", back_populates="expenses")

    internal_expense_id = None
    def __init__(self):
        print "init"
        self.is_removed = False
        self.time_stamp = datetime.utcnow()

    @classmethod
    def find_expense(cls, expense_id):
        if expense_id is None:
            return ExpenseModel()

        items = ExpenseModel.query.filter_by(expense_id=expense_id).all()

        if len(items) > 0:
            return items[0]

        return ExpenseModel()

    def configure_with_dict(self, dict_model):
        value = dict_model.get(k_title)
        if value is not None:
            self.title = value

        value = dict_model.get(k_creation_date)
        if value is not None:
            self.creation_date = parse(value)

        value = dict_model.get(k_is_removed)
        if value is not None:
            self.is_removed = value

        value = dict_model.get(k_time_stamp)
        if value is not None:
            self.time_stamp = parse(value)

        value = dict_model.get(k_internal_expense_id)
        if value is not None:
            self.internal_expense_id = value
            print "config internal id"
            print self.internal_expense_id

    def to_dict(self):
        json_object = dict()

        json_object[k_title] = self.title
        json_object[k_expense_id] = self.expense_id
        json_object[k_is_removed] = self.is_removed

        print "to dict internal id"
        print  self.internal_expense_id

        if self.internal_expense_id is not None:
            json_object[k_internal_expense_id] = self.internal_expense_id

        if self.creation_date is not None:
            json_object[k_creation_date] = self.creation_date.isoformat()

        if self.time_stamp is not None:
            json_object[k_time_stamp] = self.time_stamp.isoformat()

        return json_object
