from flask import request
from flask_restful import Resource

from SharedModels import db
from PersonModel import PersonModel
from SharedModels import docuApi as api

class RegisterUserResource(Resource):
    parser = api.parser()
    parser.add_argument('facebookID', type=str, help='Facebook ID', location='form')
    parser.add_argument('email', type=str, help='User email', location='form', required = True)
    parser.add_argument('firstName', type=str, help='First Name', location='form', required = True)
    parser.add_argument('lastName', type=str, help='Last Name', location='form', required = True)
    @api.doc(parser=parser)

    def post(self):
        personModel = PersonModel()

        personModel.facebook_id = request.form['facebookID']
        personModel.email = request.form['email']
        personModel.first_name = request.form['firstName']
        personModel.last_name = request.form['lastName']

        print request.form

        db.session.add(personModel)
        db.session.commit()

        return personModel.to_dict()

    parser = api.parser()
    parser.add_argument('userID', type=str, help='User ID', location='form', required = True)
    parser.add_argument('facebookID', type=str, help='Facebook ID', location='form')
    parser.add_argument('facebookID', type=str, help='Facebook ID', location='form')
    parser.add_argument('email', type=str, help='User email', location='form')
    parser.add_argument('firstName', type=str, help='First Name', location='form')
    parser.add_argument('lastName', type=str, help='Last Name', location='form')
    @api.doc(parser=parser)
    def put(self):
        return {"event" : "all"}