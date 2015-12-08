from flask_restful import Resource

from SharedModels import docuApi

@docuApi.route('/event/all')
class EventAllResource(Resource):
    def get(self):
        return {"event" : "all"}