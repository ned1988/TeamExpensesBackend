from flask_restful import reqparse

from SharedModels import db
from SharedModels import api
from constants import Constants
from event_model import EventModel
from PersonModel import PersonModel
from base_resource import BaseResource


class EventSynchroniseResource(BaseResource):
    parser = api.parser()
    parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
    parser.add_argument(Constants.k_user_token, type=str, help='User token', location='form', required=True)

    parser.add_argument(Constants.k_internal_id, type=str, help='Internal event ID', location='headers')
    parser.add_argument(Constants.k_event_id, type=str, help='Event ID', location='headers')
    parser.add_argument(EventModel.k_creator_id, type=str, help='Event creator ID', location='headers', required=True)
    parser.add_argument(EventModel.k_title, type=str, help='Event title', location='headers')
    parser.add_argument(EventModel.k_creation_date, type=str, help='Creation even date', location='headers')
    parser.add_argument(EventModel.k_end_date, type=str, help='End event date', location='headers')
    parser.add_argument(Constants.k_is_removed, type=str, help='Is event removed', location='headers')

    @api.doc(parser=parser)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='form', required=True)
        parser.add_argument(Constants.k_user_token, type=str, help='User token', location='form', required=True)

        parser.add_argument(Constants.k_internal_id, type=str, help='Internal event ID', location='headers')
        parser.add_argument(Constants.k_event_id, type=str, help='Event ID', location='headers')
        parser.add_argument(EventModel.k_creator_id, type=str, help='Event creator ID', location='headers',
                            required=True)
        parser.add_argument(EventModel.k_title, type=str, help='Event title', location='headers')
        parser.add_argument(EventModel.k_creation_date, type=str, help='Creation even date', location='headers')
        parser.add_argument(EventModel.k_end_date, type=str, help='End event date', location='headers')
        parser.add_argument(Constants.k_is_removed, type=str, help='Is event removed', location='headers')
        args = parser.parse_args()

        model = BaseResource.check_user_credentials_with_credentials(args[Constants.k_user_id],
                                                                     token=args[Constants.k_user_token])

        if not isinstance(model, PersonModel):
            # Return error description
            return model

        event_id = args[Constants.k_event_id]
        event_model = EventModel.find_event(event_id)
        event_model.configure_with_dict(args)

        db.session.add(event_model)
        db.session.commit()

        return event_model.event_to_dict()
