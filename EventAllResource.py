from flask_restful import Resource

class EventAllResource(Resource):
    def get(self):
        return {"event" : "all"}