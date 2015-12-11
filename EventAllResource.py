from flask_restful import Resource
from SharedModels import api

class EventAllResource(Resource):
    def get(self):
        return {"event" : "all"}

    @api.doc(responses={403: 'Not Authorized'})
    def post(self, id):
        api.abort(403)