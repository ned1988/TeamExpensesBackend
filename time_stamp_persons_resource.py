from datetime import datetime
from flask_restplus import fields
from dateutil.parser import parse
from flask_restful import reqparse

from SharedModels import api
from constants import Constants
from event_model import EventModel
from PersonModel import PersonModel
from base_resource import BaseResource
from event_team_members import EventTeamMembers

model = api.model('TimeStampPersonsResource', {
    Constants.k_result: fields.List(fields.Nested(PersonModel.swagger_return_model())),
    Constants.k_time_stamp: fields.DateTime(dt_format='ISO8601')
})


class TimeStampPersonsResource(BaseResource):
    parser = api.parser()
    parser.add_argument(Constants.k_user_id, type=str, help='User ID', location='headers', required=True)
    parser.add_argument(Constants.k_user_token, type=str, help='User token', location='headers', required=True)
    parser.add_argument(Constants.k_time_stamp, type=str, help='Time Stamp', location='headers')

    @api.doc(parser=parser)
    @api.marshal_with(model)
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

        # 2 Collect all user id's
        user_ids = set()
        for event_id in event_ids:
            event_team_members = EventTeamMembers.team_members(event_id)

            for model in event_team_members:
                user_ids.add(model.person_id)

        # 3 Collect all expenses creator id's
        for event_id in event_ids:
            event = EventModel.find_event(event_id)
            expenses = event.expenses
            [user_ids.add(expense.creator_id) for expense in expenses]

        # 4 Configure list with user information
        result = []
        for user_id in user_ids:
            person = PersonModel.time_stamp_difference(user_id, time_stamp)
            if person is not None:
                result.append(person.to_dict())

        time_stamp = datetime.utcnow()

        response = dict()
        response[Constants.k_result] = result
        response[Constants.k_time_stamp] = time_stamp.isoformat()

        return response
