from flask import request
from flask_restful import Resource

from PersonModel import PersonModel
from SharedModels import db, passlib
from SharedModels import docuApi as api
from token_serializer import TokenSerializer

class UserRegisterResource(Resource):
    parser = api.parser()
    parser.add_argument('facebookID', type=str, help='Facebook ID', location='form')
    parser.add_argument('email', type=str, help='User email', location='form', required=True)
    parser.add_argument('firstName', type=str, help='First Name', location='form', required=True)
    parser.add_argument('lastName', type=str, help='Last Name', location='form', required=True)
    parser.add_argument('password', type=str, help='Password', location='form', required=True)
    @api.doc(parser=parser)
    def post(self):
        person_model = PersonModel()
        person_model.email = request.form['email']

        items = PersonModel.query.filter_by(email=person_model.email).all()
        if len(items) > 0:
            return {'status': 'user_is_already_exist'}, 401

        person_model.facebook_id = request.form['facebookID']
        person_model.first_name = request.form['firstName']
        person_model.last_name = request.form['lastName']

        # Encrypt user password
        password = request.form['password']
        encr_password = passlib.encrypt(password, salt_length=100)
        person_model.password = encr_password

        # Generate user token with expiration date
        person_model.token = TokenSerializer.generate_auth_token(person_model.person_id)

        # Add person to the model
        db.session.add(person_model)
        db.session.commit()

        return person_model.to_dict()

    parser = api.parser()
    parser.add_argument('userID', type=int, help='User ID', location='form', required = True)
    parser.add_argument('token', type=str, help='User token', location='form', required = True)
    parser.add_argument('facebookID', type=str, help='Facebook ID', location='form')
    parser.add_argument('facebookID', type=str, help='Facebook ID', location='form')
    parser.add_argument('email', type=str, help='User email', location='form')
    parser.add_argument('firstName', type=str, help='First Name', location='form')
    parser.add_argument('lastName', type=str, help='Last Name', location='form')
    @api.doc(parser=parser)
    def put(self):
        return {"event" : "all"}