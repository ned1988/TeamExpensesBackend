from flask import request

from SharedModels import api
from constants import Constants
from event_model import EventModel
from PersonModel import PersonModel
from base_resource import BaseResource

class TimeStampResource(BaseResource):
    parser = api.parser()
    parser.add_argument('userID', type=int, help='User ID', location='headers', required=True)
    parser.add_argument('dataVersion', type=int, help='Data Version', location='headers', required=True)
    parser.add_argument('userToken', type=str, help='User token', location='headers', required=True)

    @api.doc(parser=parser)
    def get(self):
        keys = request.headers.keys()

        parameter = 'userID'
        if not parameter in keys:
            return Constants.error_missed_parameter(parameter)

        parameter = 'userToken'
        if not parameter in keys:
            return Constants.error_missed_parameter(parameter)

        parameter = 'dataVersion'
        if not parameter in keys:
            return Constants.error_missed_parameter(parameter)

        user_id = request.headers.get('userID')
        token = request.headers.get('userToken')

        model = BaseResource.check_user_credentials_with_credentials(user_id, token)

        if not isinstance(model, PersonModel):
            # Some error happens here
            return model

        data_version = request.headers.get('dataVersion')
        items = EventModel.data_version_difference(user_id, data_version)

        result = []
        for model in items:
            result.append(model.to_dict())

        return result