from flask_restful import Resource
from flask_restplus import Api
from SharedModels import docuApi

@docuApi.route('/my-resource/<id>', endpoint='my-resource')
@docuApi.doc(params={'id': 'An ID'})
class EventAllResource(Resource):
    def get(self):
        return {"event" : "all"}

    @docuApi.doc(responses={403: 'Not Authorized'})
    def post(self, id):
        docuApi.abort(403)