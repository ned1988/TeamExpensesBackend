from flask import request
from flask_restful import reqparse
from flask_restful import Resource
from itsdangerous import BadSignature, SignatureExpired

from constants import Constants
from PersonModel import PersonModel
from token_serializer import TokenSerializer


class BaseResource(Resource):
    @staticmethod
    def check_user_credentials_with_credentials(user_id, token):
        # Check token status
        status = TokenSerializer.verify_auth_token(token, user_id)

        # Is token is expired?
        if status == SignatureExpired:
            # Yes: return error status
            return {'status': Constants.error_token_expired()}, 401
        # Is toke not valid?
        elif status == BadSignature:
            # Yes: return error status
            return {'status': Constants.error_token_not_valid()}, 401

        # Try to find user with received ID
        person_model = PersonModel.query.filter_by(person_id=user_id).first()

        # Have we user with received ID?
        if person_model is None:
            # No we haven't: return error status
            return {'status': Constants.error_no_user_id()}, 400

        # Is received token correct?
        if person_model.token != token:
            # No: return error status
            return {'status': Constants.error_token_not_valid()}, 401

        # If everything is Ok - return person model
        return person_model

    @staticmethod
    def check_user_credentials():
        # Get userID from URL query
        request_parser = reqparse.RequestParser()
        request_parser.add_argument('userID', type=str)
        args = request_parser.parse_args()
        user_id = args['userID']

        # Get user token from HTTP header
        token = request.headers.get('userToken')

        return BaseResource.check_user_credentials_with_credentials(user_id, token)
