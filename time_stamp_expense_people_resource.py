from SharedModels import db
from datetime import datetime
from dateutil.parser import parse
from flask_restplus import fields
from flask_restful import reqparse

from SharedModels import api
from constants import Constants
from event_model import EventModel
from PersonModel import PersonModel
from base_resource import BaseResource
from expense_person import ExpensePerson
from event_team_members import EventTeamMembers

model = api.model('TimeStampExpensePeopleResource', {
    Constants.k_result: fields.List(fields.Nested(ExpensePerson.swagger_return_model())),
    Constants.k_time_stamp: fields.DateTime(),
})


class TimeStampExpensePeopleResource(BaseResource):
    parser = api.parser()
    parser.add_argument(Constants.k_user_id, type=str, help='User ID', location='headers', required=True)
    parser.add_argument(Constants.k_user_token, type=str, help='User token', location='headers', required=True)
    parser.add_argument(Constants.k_time_stamp, type=str, help='Time Stamp', location='headers')

    @api.doc(parser=parser)
    @api.response(200, 'Success', model)
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

        # Parse time stamp value
        time = args[Constants.k_time_stamp]
        time_stamp = None

        if time is not None and len(time) > 0:
            time_stamp = parse(time)

        query = db.session.query(ExpensePerson)

        select = db.and_(PersonModel.person_id == ExpensePerson.person_id,
                         PersonModel.person_id == EventTeamMembers.person_id,
                         db.or_(EventTeamMembers.person_id == user_id,
                                db.and_(EventTeamMembers.event_id == EventModel.event_id,
                                        EventModel.creator_id == user_id)))

        if time_stamp is not None:
            items = query.filter(select, ExpensePerson.time_stamp > time_stamp)
        else:
            items = query.filter(select)

        time_stamp = datetime.utcnow()
        result = []

        [result.append(model.to_dict()) for model in items]

        response = dict()
        response[Constants.k_result] = result
        response[Constants.k_time_stamp] = time_stamp.isoformat()

        return response
