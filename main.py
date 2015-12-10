import os
from flask import Flask
from flask_restful import Api
from flask_passlib import LazyCryptContext
from flask_passlib.context import (werkzeug_salted_md5, werkzeug_salted_sha1, werkzeug_salted_sha256, werkzeug_salted_sha512)

from UserAllResource import UserAllResource
from EventAllResource import EventAllResource
from UserRegisterResource import UserRegisterResource
from user_get_info_resource import UserGetInfoResource
from SharedModels import db, docuApi, passlib, token_secretKey

# Create Flas application
app = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teamExpenses.db'

# Create Restful API
api = Api(app)

# Create REST API docimentation
docuApi.init_app(app)

# token_secretKey.replace(token_secretKey, app.config['SECRET_KEY'])

passlib.init_app(app, context=LazyCryptContext(
    schemes=[
        werkzeug_salted_md5,
        werkzeug_salted_sha1,
        werkzeug_salted_sha256,
        werkzeug_salted_sha512,
    ],
    default='werkzeug_salted_sha512',))

api.add_resource(EventAllResource, '/event/all')

api.add_resource(UserAllResource, '/user/all')
api.add_resource(UserGetInfoResource, '/user/id')
api.add_resource(UserRegisterResource, '/user/register')

docuApi.add_resource(EventAllResource, '/event/all')

docuApi.add_resource(UserAllResource, '/user/all')
docuApi.add_resource(UserGetInfoResource, '/user/id')
docuApi.add_resource(UserRegisterResource, '/user/register')

db.init_app(app)

with app.app_context():
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)