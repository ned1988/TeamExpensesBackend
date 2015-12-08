from flask import request
from flask_restful import Resource

from SharedModels import db
from PersonModel import PersonModel
from SharedModels import docuApi as api

@api.header('facebookID', 'Facebook ID')

class RegisterUserResource(Resource):
    @api.header('email', 'User email', required=True)
    @api.header('firstName', 'First Name', required=True)
    @api.header('lastName', 'Last Name', required=True)
    def post(self):
        personModel = PersonModel()

        personModel.facebook_id = request.form['email']
        personModel.email = request.form['email']
        personModel.firstName = request.form['firstName']
        personModel.lastName = request.form['lastName']

        db.session.add(personModel)
        # db.session.commit()

        return personModel.to_dict

    @api.header('email', 'User email')
    @api.header('firstName', 'First Name')
    @api.header('lastName', 'Last Name')
    @api.header('userID', 'User ID', required=True, type = int)
    def put(self):
        return {"event" : "all"}