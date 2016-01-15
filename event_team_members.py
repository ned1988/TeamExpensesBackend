from datetime import datetime

from SharedModels import db
from constants import Constants
from PersonModel import PersonModel


class EventTeamMembers(db.Model):
    __tablename__ = 'event_team_members'

    event_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, primary_key=True)
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    @classmethod
    def team_members(cls, event_id):
        if event_id is None or not isinstance(event_id, int):
            return []

        team_member_rows = EventTeamMembers.query.filter_by(event_id=event_id).all()

        return team_member_rows

    @classmethod
    def find_team_member_for_event(cls, event_id, person_id):
        if event_id is None or not isinstance(event_id, int):
            return None

        if person_id is None or not isinstance(person_id, int):
            return None

        items = EventTeamMembers.query.filter(EventTeamMembers.event_id == event_id,
                                              EventTeamMembers.person_id == person_id).all()
        if len(items) > 0:
            existed_model = items[0]

            return existed_model
        else:
            event_team_member = EventTeamMembers()
            event_team_member.is_removed = False
            event_team_member.time_stamp = datetime.utcnow()

            return event_team_member

    @classmethod
    def add_team_member(cls, event_model, person_model):
        if event_model is None:
            return

        if person_model is None:
            return

        items = EventTeamMembers.query.filter(event_id=event_model.event_id,
                                              person_id=person_model.person_id).all()
        if len(items) > 0:
            existed_model = items[0]
            existed_model.event_id = event_model.event_id
            existed_model.person_id = person_model.person_id

    @classmethod
    def remove_team_member(cls, event_model, person_items):
        if event_model is None:
            return

        if not isinstance(person_items, list):
            return

        for person_model in person_items:
            if isinstance(person_model, PersonModel):
                items = EventTeamMembers.query.filter(event_id=event_model.event_id,
                                                      person_id=person_model.person_id).all()
                if len(items) > 0:
                    existed_model = items[0]
                    existed_model.event_id = event_model.event_id
                    existed_model.person_id = person_model.person_id

    def to_dict(self):
        json_object = dict()

        json_object[Constants.k_event_id] = self.event_id
        json_object[PersonModel.k_person_id] = self.person_id
        json_object[Constants.k_is_removed] = self.is_removed

        if self.time_stamp is not None:
            json_object[Constants.k_time_stamp] = self.time_stamp.isoformat()

        return json_object
