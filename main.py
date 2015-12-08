import os
from flask import Flask
from flask_restful import Api

from SharedModels import db
from SharedModels import docuApi
from EventAllResource import EventAllResource
from RegisterUserResource import RegisterUserResource

# Create Flas application
app = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

# Create Restful API
api = Api(app)

# Create REST API docimentation
docuApi.init_app(app)

api.add_resource(EventAllResource, '/event/all')
docuApi.add_resource(EventAllResource, 'event/all')

api.add_resource(RegisterUserResource, '/user/register')
docuApi.add_resource(RegisterUserResource, 'user/register')

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)

    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        db.create_all()