from SharedModels import db
from PersonModel import PersonModel


class EventTeamMembers(db.Model):
    __tablename__ = 'event_team_members'

    event_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, primary_key=True)
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    @classmethod
    def team_members(cls, event_model):
        if event_model is None:
            return []

        items = EventTeamMembers.query.filter_by(event_id=event_model.event_id).all()

        return items

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