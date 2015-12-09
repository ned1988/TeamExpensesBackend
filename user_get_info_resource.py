from flask import request
from flask_restful import Resource
from itsdangerous import BadSignature, SignatureExpired

from PersonModel import PersonModel
from SharedModels import docuApi as api
from token_serializer import TokenSerializer

class UserGetInfoResource(Resource):
    parser = api.parser()
    parser.add_argument('userID', type=str, help='User email', location='files', required = True)
    parser.add_argument('token', type=str, help='First Name', location='form', required = True)
    @api.doc(parser=parser)
    def get(self):
        token = request.form['token']
        user_id = request.form['user_id']

        status = TokenSerializer.verify_auth_token(token,user_id)
        if status == SignatureExpired:
            return {'status': 'token_expired'}, 401
        elif status == BadSignature:
            return {'status': 'token_not_valid'}, 401

        items = PersonModel.query.filter_by(person_id=user_id).all()

        return {}