from flask_restful import Resource
from SharedModels import docuApi

class EventAllResource(Resource):
    def get(self):
        return {"event" : "all"}

    @docuApi.doc(responses={403: 'Not Authorized'})
    def post(self, id):
        docuApi.abort(403)