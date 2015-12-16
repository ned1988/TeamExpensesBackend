import json
from datetime import datetime
from flask_restful import reqparse

from SharedModels import db
from SharedModels import api
from constants import Constants
from PersonModel import PersonModel
from base_resource import BaseResource
from event_model import EventModel, k_event_id


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

        for event_dict in json_data:
            if isinstance(event_dict, dict):
                event_model = EventModel.find_event(event_dict[k_event_id])

                if event_model is None:
                    event_model = EventModel()

                event_model.creator_id = user_id
                event_model.configure_with_dict(event_dict)

                # Add person to the model
                db.session.add(event_model)


        print json_data

        db.session.commit()

        time_stamp = datetime.utcnow()
        return {'timeStamp':time_stamp.isoformat()}
