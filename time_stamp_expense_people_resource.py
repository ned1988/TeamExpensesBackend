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
from expense_model import ExpenseModel
from expense_person import ExpensePerson
from event_team_members import EventTeamMembers

model = api.model('TimeStampExpensePeopleResource', {
    Constants.k_result: fields.List(fields.Nested(ExpensePerson.swagger_return_model())),
    Constants.k_time_stamp: fields.DateTime(),
    Constants.k_status: fields.String()
})


class TimeStampExpensePeopleResource(BaseResource):
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

        # Parse time stamp value
        time = args[Constants.k_time_stamp]
        time_stamp = None

        if time is not None and len(time) > 0:
            time_stamp = parse(time)

        query = db.session.query(ExpensePerson)

        db_and = db.and_(ExpenseModel.event_id == EventTeamMembers.event_id,
                         EventTeamMembers.person_id == user_id,
                         EventModel.event_id == ExpenseModel.event_id,
                         ExpensePerson.expense_id == ExpenseModel.expense_id,
                         ExpenseModel.creator_id == ExpensePerson.person_id)

        if time_stamp is not None:
            items = query.filter(db_and, ExpensePerson.time_stamp > time_stamp)
        else:
            items = query.filter(db_and)

        time_stamp = datetime.utcnow()
        result = []

        [result.append(model.to_dict()) for model in items]

        response = dict()
        response[Constants.k_result] = result
        response[Constants.k_time_stamp] = time_stamp

        return response
