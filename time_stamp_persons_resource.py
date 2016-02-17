from datetime import datetime
from flask_restplus import fields
from dateutil.parser import parse
from flask_restful import reqparse

from SharedModels import db
from SharedModels import api
from constants import Constants
from event_model import EventModel
from PersonModel import PersonModel
from base_resource import BaseResource
from event_team_members import EventTeamMembers

model = api.model('TimeStampPersonsResource', {
    Constants.k_result: fields.List(fields.Nested(PersonModel.swagger_return_model())),
    Constants.k_time_stamp: fields.DateTime(),
    Constants.k_status: fields.String()
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

        select = db.and_(PersonModel.person_id == EventTeamMembers.person_id,
                         db.or_(EventTeamMembers.person_id == user_id,
                                db.and_(EventTeamMembers.event_id == EventModel.event_id,
                                        EventModel.creator_id == user_id)))

        query = db.session.query(PersonModel)
        filter = query.filter(select)

        time = args[Constants.k_time_stamp]
        if time is not None and len(time) > 0:
            time_stamp = parse(time)
            filter = filter.filter(PersonModel.time_stamp > time_stamp)

        response = dict()
        response[Constants.k_result] = [model.to_dict() for model in filter]
        response[Constants.k_time_stamp] = datetime.utcnow()

        return response
