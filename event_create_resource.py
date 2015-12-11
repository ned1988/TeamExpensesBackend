from flask import request

from SharedModels import db
from SharedModels import api
from event_model import EventModel
from PersonModel import PersonModel
from base_resource import BaseResource


class EventCreateResource(BaseResource):
    parser = api.parser()
    parser.add_argument('userID', type=int, help='User ID', location='form', required=True)
    parser.add_argument('title', type=str, help='Event title', location='form', required=True)
    parser.add_argument('userToken', type=str, help='User token', location='form', required=True)

    @api.doc(parser=parser)
    def post(self):
        user_id = request.form['userID']
        token = request.form['userToken']

        model = BaseResource.check_user_credentials_with_credentials(user_id, token)

        if not isinstance(model, PersonModel):
            return model

        event_model = EventModel()
        event_model.creator_id = user_id
        event_model.title = request.form['title']

        # Add person to the model
        db.session.add(event_model)
        db.session.commit()

        return event_model.to_dict()
