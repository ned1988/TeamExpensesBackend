from PersonModel import PersonModel
from base_resource import BaseResource
from SharedModels import docuApi as api

class UserGetInfoResource(BaseResource):
    parser = api.parser()
    parser.add_argument('userID', type=str, help='User email', required = True)
    parser.add_argument('userToken', type=str, help='User token', location='headers', required = True)
    @api.doc(parser=parser)
    def get(self):
        model = self.check_user_credentials()

        if not isinstance(model, PersonModel):
            return model

        return model.to_dict()