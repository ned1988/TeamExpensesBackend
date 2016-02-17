from datetime import datetime
from dateutil.parser import parse
from flask_restplus import fields
from sqlalchemy.orm import relationship

from SharedModels import db
from SharedModels import api
from constants import Constants
from expense_model import ExpenseModel
from event_team_members import EventTeamMembers


class EventModel(db.Model):
    __tablename__ = 'event_model'

    k_title = 'title'
    k_end_date = 'endDate'
    k_expenses = 'expenses'
    k_creator_id = 'creatorID'
    k_team_members = 'teamMembers'
    k_creation_date = 'creationDate'

    event_id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('person_model.person_id'))
    title = db.Column(db.Text)
    creation_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    time_stamp = db.Column(db.DateTime)
    is_removed = db.Column(db.Boolean)

    @classmethod
    def swagger_return_model(cls):
        swagger_model = api.model('EventModel', {
            EventModel.k_title: fields.String(required=True),
            Constants.k_event_id: fields.Integer(required=True),
            EventModel.k_creator_id: fields.Integer(required=True),
            Constants.k_is_removed: fields.Boolean(required=True),
            EventModel.k_creation_date: fields.DateTime(),
            EventModel.k_end_date: fields.DateTime(),
        })

        return swagger_model

    def __init__(self):
        self.is_removed = False
        self.time_stamp = datetime.utcnow()

    @classmethod
    def time_stamp_difference(cls, user_id, time_stamp):
        if time_stamp is None:
            items = EventModel.query.filter_by(creator_id=user_id).all()
        else:
            items = EventModel.query.filter(EventModel.creator_id == user_id,
                                            EventModel.time_stamp > time_stamp).all()

        return items

    @classmethod
    def all_user_events(cls, user_id):
        items = EventModel.query.filter_by(creator_id=user_id).all()

        return items

    @classmethod
    def find_event(cls, event_id):
        if event_id is None:
            return EventModel()

        items = EventModel.query.filter_by(event_id=event_id).all()

        if len(items) > 0:
            return items[0]

        return EventModel()

    @property
    def team_members(self):
        return EventTeamMembers.team_members(self.event_id)

    def configure_with_dict(self, dict_model):
        value = dict_model.get(self.k_title)
        if value is not None:
            self.title = value

        value = dict_model.get(EventModel.k_creator_id)
        if value is not None:
            self.creator_id = value

        value = dict_model.get(self.k_creation_date)
        if value is not None:
            self.creation_date = parse(value)

        # Update time stamp each time we update model from user
        self.time_stamp = datetime.utcnow()

    def event_to_dict(self):
        json_object = dict()

        json_object[self.k_title] = self.title
        json_object[Constants.k_event_id] = self.event_id
        json_object[self.k_creator_id] = self.creator_id
        json_object[Constants.k_is_removed] = self.is_removed

        if self.creation_date is not None:
            json_object[self.k_creation_date] = self.creation_date

        if self.end_date is not None:
            json_object[self.k_end_date] = self.end_date

        return json_object

    def to_dict(self):
        json_object = self.event_to_dict()

        return json_object

EventModel.expenses = relationship("ExpenseModel", order_by=ExpenseModel.expense_id, back_populates="event_model")
