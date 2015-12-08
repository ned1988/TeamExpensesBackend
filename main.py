import os
from flask import Flask
from flask_restful import Api
from flask_restplus import Api as restplusAPI

from SharedModels import db
from SharedModels import docuApi
from EventAllResource import EventAllResource

# Create Flas application
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

# Create Restful API
api = Api(app)
docuApi = restplusAPI(app)
api.add_resource(EventAllResource, '/event/all')

# db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
    # db.create_all()