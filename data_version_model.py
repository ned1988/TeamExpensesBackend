from SharedModels import db


class DataVersionModel(db.Model):
    data_version_id_seq = db.Sequence('data_version_id_seq')
    data_version_id = db.Column(db.Integer, data_version_id_seq, server_default=data_version_id_seq.next_value(),
                                primary_key=True)
