from flask import request
from flask_restful import Resource
from flask_restful import reqparse
from itsdangerous import BadSignature, SignatureExpired

from PersonModel import PersonModel
from SharedModels import docuApi as api
from token_serializer import TokenSerializer

class UserGetInfoResource(Resource):
    parser = api.parser()
    parser.add_argument('userID', type=str, help='User email', required = True)
    parser.add_argument('user_token', type=str, help='User token', location='headers', required = True)
    @api.doc(parser=parser)
    def get(self):
        request_parser = reqparse.RequestParser()
        request_parser.add_argument('userID', type=str)
        args = request_parser.parse_args()
        user_id = args['userID']

        token = request.headers.get('token')

        status = TokenSerializer.verify_auth_token(token, user_id)
        if status == SignatureExpired:
            return {'status': 'token_expired'}, 401
        elif status == BadSignature:
            return {'status': 'token_not_valid'}, 401

        person_model = PersonModel.query.filter_by(person_id=user_id).first()

        if person_model != None:
            return {'status': 'no_user_id'}, 400

        if person_model.token != token:
            return {'status': 'token_not_valid'}, 401

        return person_model.to_dict()