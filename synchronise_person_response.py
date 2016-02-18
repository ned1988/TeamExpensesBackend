from flask_restplus import fields
from flask_restful import reqparse

from SharedModels import db
from SharedModels import api
from constants import Constants
from PersonModel import PersonModel
from base_resource import BaseResource

model = api.model('SynchronisePersonResource', {
    Constants.k_result: fields.Nested(PersonModel.swagger_return_model()),
})


class SynchronisePersonResource(BaseResource):
    parser = api.parser()
    parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
    parser.add_argument(Constants.k_user_token, type=str, help='User token', location='form', required=True)

    parser.add_argument(PersonModel.k_person_id, type=str, help='Person ID', location='headers')
    parser.add_argument(Constants.k_internal_id, type=str, help='Internal event ID', location='headers')
    parser.add_argument(Constants.k_is_removed, type=str, help='Is person removed from event', location='headers')

    parser.add_argument(PersonModel.k_first_name, type=str, help='First name', location='headers')
    parser.add_argument(PersonModel.k_last_name, type=str, help='Last name', location='headers')
    parser.add_argument(PersonModel.k_email, type=str, help='Email', location='headers')
    parser.add_argument(PersonModel.k_facebook_id, type=str, help='Facebook ID', location='headers')

    @api.doc(parser=parser)
    @api.response(200, 'Success', model)
    @api.response(401, 'Error', Constants.error_login_response())
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
        parser.add_argument(Constants.k_user_token, type=str, help='User token', location='form', required=True)

        parser.add_argument(PersonModel.k_person_id, type=str, help='Person ID', location='headers')
        parser.add_argument(Constants.k_internal_id, type=str, help='Internal event ID', location='headers')
        parser.add_argument(Constants.k_is_removed, type=str, help='Is person removed from event', location='headers')

        parser.add_argument(PersonModel.k_first_name, type=str, help='First name', location='headers')
        parser.add_argument(PersonModel.k_last_name, type=str, help='Last name', location='headers')
        parser.add_argument(PersonModel.k_email, type=str, help='Email', location='headers')
        parser.add_argument(PersonModel.k_facebook_id, type=str, help='Facebook ID', location='headers')
        args = parser.parse_args()

        user_id = args[Constants.k_user_id]
        token = args[Constants.k_user_token]
        current_user = BaseResource.check_user_credentials_with_credentials(user_id, token=token)

        if not isinstance(current_user, PersonModel):
            # Return error description
            return current_user

        email = args.get(PersonModel.k_email)

        # Is person has email?
        if email is not None and len(email) > 0:
            # Yes: try to find person by email
            person = PersonModel.find_person_by_email(email)
            if person is not None:
                # Person with this email is exist
                person.configure_with_dict(args)
            else:
                # Person with current email doesn't exist
                person = PersonModel()
        else:
            # No: try to find the person by ID
            person_id = args.get(PersonModel.k_person_id)
            person = PersonModel.find_person(person_id)

        person.configure_with_dict(args)

        db.session.add(person)
        db.session.commit()

        result = dict()
        result[Constants.k_result] = person.to_dict()

        return result
