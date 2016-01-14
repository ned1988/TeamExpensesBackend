import os
from flask import Flask
from flask_restful import Api
from flask_passlib import LazyCryptContext
from flask_passlib.context import werkzeug_salted_md5
from flask_passlib.context import werkzeug_salted_sha1
from flask_passlib.context import werkzeug_salted_sha256
from flask_passlib.context import werkzeug_salted_sha512

from SharedModels import db, passlib
from SharedModels import api as docu_api
from EventAllResource import EventAllResource
from time_stamp_resource import TimeStampResource
from user_login_resource import UserLoginResource
from synchronise_resource import SynchroniseResponse
from event_create_resource import EventCreateResource
from UserRegisterResource import UserRegisterResource
from user_get_info_resource import UserGetInfoResource
from event_synchronise_resource import EventSynchroniseResource
from synchronise_person_response import SynchronisePersonResource
from synchronise_expense_resource import SynchroniseExpenseResource
from event_add_team_members_resource import EventAddTeamMembersResource

os.environ.setdefault("DATABASE_URL", "postgresql://localhost/postgres")

# Create Flask application
app = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

# Create Restful API
api = Api(app)

# Create REST API documentation
docu_api.init_app(app)

# token_secretKey.replace(token_secretKey, app.config['SECRET_KEY'])

passlib.init_app(app, context=LazyCryptContext(
    schemes=[
        werkzeug_salted_md5,
        werkzeug_salted_sha1,
        werkzeug_salted_sha256,
        werkzeug_salted_sha512,
    ],
    default='werkzeug_salted_sha512',))

# Resources

api.add_resource(TimeStampResource, '/timeStamp')
api.add_resource(SynchroniseResponse, '/synchronise')
api.add_resource(EventSynchroniseResource, '/synchronise/event')
api.add_resource(SynchroniseExpenseResource, '/synchronise/expense')
api.add_resource(SynchronisePersonResource, '/synchronise/teamMember')

api.add_resource(EventAllResource, '/event/all')
api.add_resource(EventCreateResource, '/event/create')
api.add_resource(EventAddTeamMembersResource, '/event/addTeamMembers')

api.add_resource(UserGetInfoResource, '/user')
api.add_resource(UserLoginResource, '/user/login')
api.add_resource(UserRegisterResource, '/user/register')

# REST API documentation

docu_api.add_resource(TimeStampResource, '/timeStamp')
docu_api.add_resource(SynchroniseResponse, '/synchronise')
docu_api.add_resource(EventSynchroniseResource, '/synchronise/event')
docu_api.add_resource(SynchroniseExpenseResource, '/synchronise/expense')
docu_api.add_resource(SynchronisePersonResource, '/synchronise/teamMember')

docu_api.add_resource(EventAllResource, '/event/all')
docu_api.add_resource(EventCreateResource, '/event/create')
docu_api.add_resource(EventAddTeamMembersResource, '/event/addTeamMembers')

docu_api.add_resource(UserGetInfoResource, '/user')
docu_api.add_resource(UserLoginResource, '/user/login')
docu_api.add_resource(UserRegisterResource, '/user/register')

db.init_app(app)

with app.app_context():
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
