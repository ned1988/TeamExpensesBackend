from flask import request
from flask_restful import reqparse

from SharedModels import api
from event_model import EventModel
from PersonModel import PersonModel
from base_resource import BaseResource


class EventAllResource(BaseResource):
    parser = api.parser()
    parser.add_argument('userID', type=str, help='User ID', required=True)
    parser.add_argument('eventID', type=str, help='Event ID', location='headers', required=True)
    parser.add_argument('userToken', type=str, help='User token', location='headers', required=True)

    @api.doc(parser=parser)
    def get(self):
        # Get userID from URL query
        request_parser = reqparse.RequestParser()
        request_parser.add_argument('userID', type=str)
        args = request_parser.parse_args()
        user_id = args['userID']

        token = request.form['userToken']
        event_id = request.form['eventID']

        model = BaseResource.check_user_credentials_with_credentials(user_id, token)

        if not isinstance(model, PersonModel):
            # Some error happens here
            return model

        # person_model = EventModel.query.filter_by(creator_id=email).all()
        return {"event" : "all"}

    @api.doc(responses={403: 'Not Authorized'})
    def put(self, id):
        api.abort(403)