import json
from datetime import datetime
from flask_restful import reqparse

from SharedModels import db
from SharedModels import api
from constants import Constants
from event_model import EventModel
from PersonModel import PersonModel
from base_resource import BaseResource


class SynchroniseResponse(BaseResource):
    parser = api.parser()
    parser.add_argument('userID', type=str, help='User ID', location='form', required=True)
    parser.add_argument('userData', type=str, help='User Data', location='form', required=True)
    parser.add_argument('userToken', type=str, help='User Token', location='form', required=True)

    @api.doc(parser=parser)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userID', type=str, help='User ID', location='form', required=True)
        parser.add_argument('userData', type=str, help='User Data', location='form', required=True)
        parser.add_argument('userToken', type=str, help='User Token', location='form', required=True)
        args = parser.parse_args()

        user_id = args['userID']
        token = args['userToken']

        model = BaseResource.check_user_credentials_with_credentials(user_id, token)

        if not isinstance(model, PersonModel):
            # Some error happens here
            return model

        json_data = args['userData']

        try:
            json_data = json.loads(json_data)
        except ValueError:
            return Constants.error_wrong_json_format()

        if not isinstance(json_data, list):
            return Constants.error_wrong_json_structure()

        print json_data

        result = []
        for event_dict in json_data:
            if isinstance(event_dict, dict):
                event_model = EventModel.find_event(event_dict.get(EventModel.k_event_id))

                event_model.creator_id = user_id
                event_model.configure_with_dict(event_dict)

                db.session.add(event_model)
                db.session.commit()

                event_json = event_model.to_dict()

                result.append(event_json)

        time_stamp = datetime.utcnow()
        response = dict()
        response[Constants.k_time_stamp] = time_stamp.isoformat()
        response['result'] = result

        return response
