__author__ = 'Denys.Meloshyn'

from flask import Flask
from flask_restplus import Api

from flask_restful import reqparse
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

docuApi = Api()

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)