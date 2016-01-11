from sqlalchemy import orm
from datetime import datetime
from dateutil.parser import parse
from sqlalchemy.orm import relationship

from SharedModels import db
from expense_model import ExpenseModel
from expense_model import k_expense_id, k_internal_expense_id

k_title = 'title'
k_event_id = 'eventID'
k_expenses = 'expenses'
k_internal_event_id = 'internalID'


class EventModel(db.Model):
    __tablename__ = 'event_model'

    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    creator_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    time_stamp = db.Column(db.DateTime)
    is_removed = db.Column(db.Boolean)

    # Many to many relationship
    secondary_table = db.Table('event_personal', db.Model.metadata,
                               db.Column('event_id', db.Integer, db.ForeignKey('event_model.event_id'), primary_key=True),
                               db.Column('person_id', db.Integer, db.ForeignKey('person_model.person_id'), primary_key=True))
    team_members = relationship('PersonModel', secondary=secondary_table, backref='events')

    def __init__(self):
        self.is_removed = False
        self.time_stamp = datetime.utcnow()

    @orm.reconstructor
    def init_on_load(self):
        self.internal_event_id = None
        self.internal_expense_ids = {}

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
        if event_id is None:
            return EventModel()

        items = EventModel.query.filter_by(event_id=event_id).all()

        if len(items) > 0:
            return items[0]

        return EventModel()

    def configure_with_dict(self, dict_model):
        value = dict_model.get(k_title)
        if value is not None:
            self.title = value

        value = dict_model.get(k_internal_event_id)
        if value is not None:
            self.internal_event_id = value

        value = dict_model.get('creationDate')
        if value is not None:
            self.creation_date = parse(value)

        value = dict_model.get('timeStamp')
        if value is not None:
            self.time_stamp = parse(value)

        value = dict_model.get(k_expenses)
        if value is not None and isinstance(value, list):
            result = list(self.expenses)
            for expense_dict in value:
                expense_id = expense_dict.get(k_expense_id)

                expense = ExpenseModel.find_expense(expense_id)
                expense.configure_with_dict(expense_dict)

                # Need commit immediately to get 'expense_id'
                db.session.add(expense)
                db.session.commit()

                if k_internal_expense_id in expense_dict:
                    self.internal_expense_ids[expense.expense_id] = expense_dict[k_internal_expense_id]

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

        if self.internal_event_id is not None:
            json_object[k_internal_event_id] = self.internal_event_id

        expense_items = []
        for model in self.expenses:
            if model.expense_id in self.internal_expense_ids:
                model.internal_expense_id = self.internal_expense_ids[model.expense_id]
            expense_items.append(model.to_dict())
        json_object[k_expenses] = expense_items

        return json_object

EventModel.expenses = relationship("ExpenseModel", order_by=ExpenseModel.expense_id, back_populates="event_model")