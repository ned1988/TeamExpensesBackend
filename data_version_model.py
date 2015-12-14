from SharedModels import db
from sqlalchemy import create_engine


class DataVersionModel(db.Model):
    data_version_id = db.Column(db.Integer,  db.Sequence('data_version_id',start=1), primary_key=True)

    def data_version(self):
        engine = create_engine('postgresql://localhost/Denys.Meloshyn')
        connection = engine.connect()
        seq = db.Sequence('data_version_id')
        nextid = connection.execute(seq)

        return nextid
