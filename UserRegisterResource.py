from flask_restplus import fields
from flask_restful import reqparse
from flask_restful import Resource

from SharedModels import api
from constants import Constants
from PersonModel import PersonModel
from SharedModels import db, passlib
from token_serializer import TokenSerializer

model = api.model('UserRegisterResource', {
    Constants.k_user: fields.Nested(PersonModel.swagger_return_model()),
    Constants.k_status: fields.String()
})


class UserRegisterResource(Resource):
    parser = api.parser()
    parser.add_argument('email', type=str, help='User email', location='form', required=True)
    parser.add_argument('firstName', type=str, help='First Name', location='form', required=True)
    parser.add_argument('lastName', type=str, help='Last Name', location='form', required=True)
    parser.add_argument('password', type=str, help='Password', location='form', required=True)
    parser.add_argument('facebookID', type=str, help='Facebook ID', location='form')

    @api.doc(parser=parser)
    @api.response(200, 'Success', model)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='User email', location='form', required=True)
        parser.add_argument('firstName', type=str, help='First Name', location='form', required=True)
        parser.add_argument('lastName', type=str, help='Last Name', location='form', required=True)
        parser.add_argument('password', type=str, help='Password', location='form', required=True)
        parser.add_argument('facebookID', type=str, help='Facebook ID', location='form')
        args = parser.parse_args()

        person_model = PersonModel()
        person_model.configure_with_dict(args)

        items = PersonModel.query.filter_by(email=person_model.email).all()
        if len(items) > 0:
            return Constants.error_with_message_and_status('user_is_already_exist', 401)

        # Encrypt user password
        password = args['password']
        encrypted_password = passlib.encrypt(password, salt_length=100)
        person_model.password = encrypted_password

        # Generate user token with expiration date
        person_model.token = TokenSerializer.generate_auth_token(person_model.person_id)

        # Add person to the model
        db.session.add(person_model)
        db.session.commit()

        result = dict()
        result[Constants.k_status] = Constants.k_user_credentials_correct
        result[Constants.k_user] = person_model.to_dict()

        return result
