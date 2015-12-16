from dateutil.parser import parse
from flask_restful import reqparse

from SharedModels import api
from event_model import EventModel
from PersonModel import PersonModel
from base_resource import BaseResource


class TimeStampResource(BaseResource):
    parser = api.parser()
    parser.add_argument('userID', type=str, help='User ID', location='headers', required=True)
    parser.add_argument('timeStamp', type=str, help='Time Stamp', location='headers', required=True)
    parser.add_argument('userToken', type=str, help='User token', location='headers', required=True)

    @api.doc(parser=parser)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userID', type=str, help='User ID', location='headers', required=True)
        parser.add_argument('timeStamp', type=str, help='Time Stamp', location='headers', required=True)
        parser.add_argument('userToken', type=str, help='User token', location='headers', required=True)

        args = parser.parse_args()
        user_id = args['userID']
        token = args['userToken']

        model = BaseResource.check_user_credentials_with_credentials(user_id, token)

        if not isinstance(model, PersonModel):
            # Some error happens here
            return model

        time = args['timeStamp']
        time_stamp = None
        if len(time) > 0:
            time_stamp = parse(time)

        items = EventModel.time_stamp_difference(user_id, time_stamp)
        print items
        result = [result_model.to_dict() for result_model in items]
        print result

        return result
