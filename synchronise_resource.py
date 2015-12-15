from flask import request

from SharedModels import api
from constants import Constants
from PersonModel import PersonModel
from base_resource import BaseResource


class SynchroniseResponse(BaseResource):
    parser = api.parser()
    parser.add_argument('userID', type=int, help='User ID', location='form', required=True)
    parser.add_argument('timeStamp', type=str, help='Time Stamp', location='form', required=True)
    parser.add_argument('userToken', type=str, help='User Token', location='form', required=True)

    @api.doc(parser=parser)
    def get(self):
        keys = request.headers.keys()

        parameter = 'userID'
        if parameter not in keys:
            return Constants.error_missed_parameter(parameter)

        parameter = 'userToken'
        if parameter not in keys:
            return Constants.error_missed_parameter(parameter)

        parameter = 'timeStamp'
        if parameter not in keys:
            return Constants.error_missed_parameter(parameter)

        user_id = request.headers.get('userID')
        token = request.headers.get('userToken')

        model = BaseResource.check_user_credentials_with_credentials(user_id, token)

        if not isinstance(model, PersonModel):
            # Some error happens here
            return model

        return {}
