from datetime import datetime
from dateutil.parser import parse
from flask_restful import reqparse

from SharedModels import api
from constants import Constants
from event_model import EventModel
from PersonModel import PersonModel
from base_resource import BaseResource
from event_team_members import EventTeamMembers


class TimeStampTeamMembersResource(BaseResource):
    parser = api.parser()
    parser.add_argument(Constants.k_user_id, type=str, help='User ID', location='headers', required=True)
    parser.add_argument(Constants.k_user_token, type=str, help='User token', location='headers', required=True)
    parser.add_argument(Constants.k_time_stamp, type=str, help='Time Stamp', location='headers')

    @api.doc(parser=parser)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(Constants.k_user_id, type=str, help='User ID', location='headers', required=True)
        parser.add_argument(Constants.k_user_token, type=str, help='User token', location='headers', required=True)
        parser.add_argument(Constants.k_time_stamp, type=str, help='Time Stamp', location='headers')
        args = parser.parse_args()

        user_id = args[Constants.k_user_id]
        token = args[Constants.k_user_token]
        model = BaseResource.check_user_credentials_with_credentials(user_id, token)

        if not isinstance(model, PersonModel):
            # Wrong user credentials
            return model

        # 1 First of all we need to find ell interested us events:
        # - it can be created by current user
        # - user can be the team member in event
        event_ids = set()

        # All events where user is a creator
        items = EventModel.all_user_events(user_id)
        for event_model in items:
            event_ids.add(event_model.event_id)

        # All events where user is a team member
        items = EventTeamMembers.find_rows_for_user(user_id)
        for event_team_member_model in items:
            event_ids.add(event_team_member_model.event_id)

        time = args[Constants.k_time_stamp]
        time_stamp = None
        if time is not None and len(time) > 0:
            time_stamp = parse(time)

        # 2 Now wee need to collect information about all team members
        result = []
        user_ids = set()
        for event_id in event_ids:
            event_team_members = EventTeamMembers.time_stamp_for_event(event_id, time_stamp)

            for model in event_team_members:
                result.append(model.to_dict())
                user_ids.add(model.person_id)

        time_stamp = datetime.utcnow()

        response = dict()
        response[Constants.k_result] = result
        response[Constants.k_time_stamp] = time_stamp.isoformat()

        return response
