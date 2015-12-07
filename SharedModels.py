__author__ = 'Denys.Meloshyn'

from flask_restful import reqparse
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)