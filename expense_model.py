from sqlalchemy import orm
from datetime import datetime
from dateutil.parser import parse
from sqlalchemy.orm import relationship

from SharedModels import db
from constants import Constants

class ExpenseModel(db.Model):
    k_title = 'title'
    k_value = 'value'
    k_time_stamp = 'timeStamp'
    k_expense_id = 'expenseID'
    k_creator_id = 'creatorID'
    k_creation_date = 'creationDate'

    __tablename__ = 'expense_model'

    expense_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    value = db.Column(db.Float)
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)
    creation_date = db.Column(db.DateTime)
    creator_id = db.Column(db.Integer)

    # One to many relationship
    event_id = db.Column(db.Integer, db.ForeignKey('event_model.event_id'))
    event_model = relationship("EventModel", back_populates="expenses")

    def __init__(self):
        self.is_removed = False
        self.time_stamp = datetime.utcnow()

    @orm.reconstructor
    def init_on_load(self):
        self.internal_expense_id = None

    @classmethod
    def time_stamp_difference(cls, event_id, time_stamp):
        if time_stamp is None:
            rows = ExpenseModel.query.filter_by(event_id=event_id).all()
        else:
            rows = ExpenseModel.query.filter(ExpenseModel.event_id == event_id,
                                              ExpenseModel.time_stamp > time_stamp).all()
        return rows

    @classmethod
    def find_expense(cls, expense_id):
        if expense_id is None:
            return ExpenseModel()

        items = ExpenseModel.query.filter_by(expense_id=expense_id).all()

        if len(items) > 0:
            return items[0]

        return ExpenseModel()

    def configure_with_dict(self, dict_model):
        value = dict_model.get(ExpenseModel.k_title)
        if value is not None:
            self.title = value

        value = dict_model.get(ExpenseModel.k_creator_id)
        if value is not None:
            self.creator_id = value

        value = dict_model.get(Constants.k_event_id)
        if value is not None:
            self.event_id = value

        value = dict_model.get(ExpenseModel.k_value)
        if value is not None:
            self.value = value

        value = dict_model.get(ExpenseModel.k_creation_date)
        if value is not None:
            self.creation_date = parse(value)

        value = dict_model.get(Constants.k_is_removed)
        if value is not None:
            self.is_removed = value

        value = dict_model.get(Constants.k_internal_id)
        if value is not None:
            self.internal_expense_id = value

        # Update time stamp each time we update model from user
        self.time_stamp = datetime.utcnow()

    def to_dict(self):
        json_object = dict()

        json_object[ExpenseModel.k_title] = self.title
        json_object[ExpenseModel.k_value] = self.value
        json_object[Constants.k_event_id] = self.event_id
        json_object[Constants.k_is_removed] = self.is_removed
        json_object[ExpenseModel.k_expense_id] = self.expense_id
        json_object[ExpenseModel.k_creator_id] = self.creator_id

        if self.creation_date is not None:
            json_object[ExpenseModel.k_creation_date] = self.creation_date.isoformat()

        return json_object
