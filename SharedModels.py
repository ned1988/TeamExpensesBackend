__author__ = 'Denys.Meloshyn'

from flask_restplus import Api
from flask_passlib import Passlib
from flask_restful import reqparse
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
passlib = Passlib()
docuApi = Api()

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)