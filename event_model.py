from sqlalchemy import orm
from datetime import datetime
from dateutil.parser import parse
from sqlalchemy.orm import relationship

from SharedModels import db
from constants import Constants
from expense_model import ExpenseModel
from expense_model import k_expense_id
from PersonModel import PersonModel, k_personID

k_title = 'title'
k_end_date = 'endDate'
k_event_id = 'eventID'
k_expenses = 'expenses'
k_creator_id = 'creatorID'
k_is_removed = 'isRemoved'
k_time_stamp = 'timeStamp'
k_creation_date = 'creationDate'


class EventModel(db.Model):
    __tablename__ = 'event_model'

    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    creation_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    time_stamp = db.Column(db.DateTime)
    is_removed = db.Column(db.Boolean)

    # One person can create many events
    creator_id = db.Column(db.Integer, db.ForeignKey('person_model.person_id'))

    # Many Events can have many different team members and reverse
    secondary_table = db.Table('event_personal', db.Model.metadata,
                               db.Column('event_id', db.Integer, db.ForeignKey('event_model.event_id'), primary_key=True),
                               db.Column('person_id', db.Integer, db.ForeignKey('person_model.person_id'), primary_key=True))
    team_members = relationship('PersonModel', secondary=secondary_table, backref='events_team_member')

    def __init__(self):
        self.is_removed = False
        self.time_stamp = datetime.utcnow()

    @orm.reconstructor
    def init_on_load(self):
        self.internal_event_id = None
        self.internal_expense_ids = {}
        self.internal_team_member_ids = {}

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

        value = dict_model.get(Constants.k_internal_id)
        if value is not None:
            self.internal_event_id = value

        value = dict_model.get(k_creation_date)
        if value is not None:
            self.creation_date = parse(value)

        value = dict_model.get(k_expenses)
        self.configure_expense_with_dict(value)

    def configure_expense_with_dict(self, dict_model):
        if dict_model is not None and isinstance(dict_model, list):
            result = list(self.expenses)
            for expense_dict in dict_model:
                expense_id = expense_dict.get(k_expense_id)

                expense = ExpenseModel.find_expense(expense_id)
                expense.configure_with_dict(expense_dict)

                # Need commit immediately to get 'expense_id'
                db.session.add(expense)
                db.session.commit()

                if Constants.k_internal_id in expense_dict:
                    self.internal_expense_ids[expense.expense_id] = expense_dict[Constants.k_internal_id]

                result.append(expense)
            self.expenses = result

    def configure_team_members_with_dict(self, dict_model):
        if dict_model is not None and isinstance(dict_model, list):
            result = list(self.team_members)
            for member_dict in dict_model:
                member_id = member_dict.get(k_personID)

                member = PersonModel.find_person(member_id)
                member.configure_with_dict(member_dict)

                # Need commit immediately to get 'person_id'
                db.session.add(member)
                db.session.commit()

                if Constants.k_internal_id in member_dict:
                    self.internal_team_member_ids[member.person_id] = member_dict[Constants.k_internal_id]

                result.append(member)
            self.team_members = result

    def to_dict(self):
        json_object = dict()

        json_object[k_title] = self.title
        json_object[k_event_id] = self.event_id
        json_object[k_creator_id] = self.creator_id
        json_object[k_is_removed] = self.is_removed

        if self.creation_date is not None:
            json_object[k_creation_date] = self.creation_date.isoformat()

        if self.end_date is not None:
            json_object[k_end_date] = self.end_date.isoformat()

        if self.time_stamp is not None:
            json_object[k_time_stamp] = self.time_stamp.isoformat()

        if self.internal_event_id is not None:
            json_object[Constants.k_internal_id] = self.internal_event_id

        result = []
        for model in self.expenses:
            if model.expense_id in self.internal_expense_ids:
                model.internal_expense_id = self.internal_expense_ids[model.expense_id]
            result.append(model.to_dict())
        json_object[k_expenses] = result

        result = []
        for model in self.team_members:
            if model.person_id in self.internal_team_member_ids:
                model.internal_person_id = self.internal_team_member_ids[model.person_id]
            result.append(model.to_dict())
        json_object[k_expenses] = result

        return json_object

EventModel.expenses = relationship("ExpenseModel", order_by=ExpenseModel.expense_id, back_populates="event_model")