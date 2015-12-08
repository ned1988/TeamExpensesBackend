import os
from flask import Flask
from flask_restful import Api

from SharedModels import db
from EventAllResource import EventAllResource

# Create Flas application
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

# Create Restful API
api = Api(app)
api.add_resource(EventAllResource, '/events/all')

# db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
    # db.create_all()