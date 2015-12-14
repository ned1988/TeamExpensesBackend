import os
from SharedModels import db
from sqlalchemy import create_engine


class DataVersionModel(db.Model):
    data_version_id = db.Column(db.Integer,  db.Sequence('data_version_id',start=1), primary_key=True)

    @staticmethod
    def data_version():
        engine = create_engine(os.environ['DATABASE_URL'])
        connection = engine.connect()
        seq = db.Sequence('data_version_id')
        nextid = connection.execute(seq)
        connection.close()

        return nextid
