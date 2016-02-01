from datetime import datetime
from flask_restful import reqparse

from SharedModels import db
from SharedModels import api
from constants import Constants
from PersonModel import PersonModel
from base_resource import BaseResource
from event_team_members import EventTeamMembers


class SynchroniseTeamMemberResource(BaseResource):
    parser = api.parser()
    parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
    parser.add_argument(Constants.k_user_token, type=str, help='User token', location='form', required=True)

    parser.add_argument(Constants.k_event_id, type=int, help='Event ID', location='headers', required=True)
    parser.add_argument(PersonModel.k_person_id, type=int, help='Person ID', location='headers', required=True)
    parser.add_argument(EventTeamMembers.k_team_member_id, type=int, help='Team member ID', location='headers')
    parser.add_argument(Constants.k_is_removed, type=str, help='Is team member removed from event', location='headers')

    @api.doc(parser=parser)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)

        parser.add_argument(Constants.k_user_token, type=str, help='User token', location='form', required=True)
        parser.add_argument(Constants.k_event_id, type=int, help='Team Member ID', location='headers', required=True)
        parser.add_argument(PersonModel.k_person_id, type=int, help='Person ID', location='headers', required=True)
        parser.add_argument(EventTeamMembers.k_team_member_id, type=int, help='Team member ID', location='headers')
        parser.add_argument(Constants.k_is_removed, type=str, help='Is person removed from event', location='headers')
        args = parser.parse_args()

        user_id = args[Constants.k_user_id]
        token = args[Constants.k_user_token]
        current_user = BaseResource.check_user_credentials_with_credentials(user_id, token=token)

        if not isinstance(current_user, PersonModel):
            # Return error description
            return current_user

        team_member = EventTeamMembers.find_team_member(args[EventTeamMembers.k_team_member_id])
        team_member.configure_with_dict(args)

        db.session.add(team_member)
        db.session.commit()

        return team_member.to_dict()
