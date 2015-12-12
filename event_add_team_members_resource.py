import json
from flask import request
from SharedModels import db
from SharedModels import api
from event_model import EventModel
from PersonModel import PersonModel
from base_resource import BaseResource


class EventAddTeamMembersResource(BaseResource):
    parser = api.parser()
    # parser.add_argument('userID', type=int, help='User ID', location='form', required=True)
    # parser.add_argument('eventID', type=int, help='Event ID', location='form', required=True)
    # parser.add_argument('userToken', type=str, help='User token', location='form', required=True)
    parser.add_argument('teamMembersID', type=str, help='Users IDs', location='form', required=True)

    @api.doc(parser=parser)
    def post(self):
        # user_id = request.form['userID']
        # token = request.form['userToken']
        # event_id = request.form['eventID']

        # model = BaseResource.check_user_credentials_with_credentials(user_id, token)
        #
        # if not isinstance(model, PersonModel):
        #     return model

        # items = EventModel.query.filter_by(event_id=event_id).all()
        # if len(items) > 0:
        #     return {'status': 'event_not_exist'}, 401

        team_members_json = request.form['teamMembersID']

        try:
            team_members = json.loads(team_members_json)
        except ValueError:
            return {'status': 'wrong_json_format'}, 401

        if not isinstance(team_members, list):
            return {'status': 'wrong_json_structure'}, 401

        result = {}
        for team_member in team_members:
            person_model = PersonModel()

            # Add person to the model
            db.session.add(person_model)
            db.session.commit()

            result[team_member] = person_model.person_id

        return result
