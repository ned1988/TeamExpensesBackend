from flask import request
from flask_restful import Resource

from SharedModels import db
from SharedModels import passlib
from PersonModel import PersonModel
from SharedModels import docuApi as api
from token_serializer import TokenSerializer

class UserLoginResource(Resource):
    parser = api.parser()
    parser.add_argument('email', type=str, help='User email', location='form', required=True)
    parser.add_argument('password', type=str, help='User password', location='form', required=True)
    @api.doc(parser=parser)
    def post(self):
        email = request.form['email']
        password = request.form['password']

        person_model = PersonModel.query.filter_by(email=email).first()
        if person_model != None:
            if passlib.verify(password, person_model.password):
                person_model.token = TokenSerializer.generate_auth_token(person_model.person_id)
                db.session.commit()

                return  person_model.to_dict()
            else:
                return {'status': 'user_password_is_wrong'}, 401
        else:
            return {'status': 'user_is_not_exist'}, 401