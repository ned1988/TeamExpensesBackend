from flask import request
from SharedModels import api
from dateutil.parser import parse
from event_model import EventModel
from base_resource import BaseResource

class TimeStampResource(BaseResource):
    parser = api.parser()
    parser.add_argument('userID', type=int, help='User ID', location='headers', required=True)
    parser.add_argument('timeStamp', type=str, help='Time Stamp', location='headers', required=True)
    # parser.add_argument('userToken', type=str, help='User token', location='headers', required=True)

    @api.doc(parser=parser)
    def get(self):
        user_id = request.headers.get('userID')
        # token = request.headers.get('userToken')
        # event_id = request.form['eventID']

        # model = BaseResource.check_user_credentials_with_credentials(user_id, token)
        #
        # if not isinstance(model, PersonModel):
        #     # Some error happens here
        #     return model

        time_stamp = parse(request.headers.get('timeStamp'))
        items = EventModel.time_stamp_difference(user_id, time_stamp)

        result = []
        for model in items:
            result.append(model.to_dict())

        return result