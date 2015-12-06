from flask import Flask
from flask_restful import Api

from EventAllResource import EventAllResource

# Create Flas application
app = Flask(__name__)

# Create Restful API
api = Api(app)

api.add_resource(EventAllResource, '/events/all')

if __name__ == '__main__':
    app.run(debug=True)