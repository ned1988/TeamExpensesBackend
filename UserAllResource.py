from flask_restful import Resource

from PersonModel import PersonModel

class UserAllResource(Resource):
    def get(self):
        items = PersonModel.query.all()
        json_result = [person_model.to_dict() for person_model in items]

        return json_result