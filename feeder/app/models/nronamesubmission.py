"""Name hold a name choice for a Request
"""
from app import db


class NRONameSubmission(db.Model):
    __bind_key__ = 'nro_db'
    __table_args__ = {"schema": "bc_registries_names"}
    __tablename__ = 'name_submission_info'

    # nr_num = db.Column('nr_num', db.String(10))
    choice = db.Column('choice_number', db.Integer)
    name = db.Column(db.String(150))
    corp_num = db.Column('corp_num', db.String(10))
    consumption_date = db.Column('consumption_date', db.DateTime)
    state = db.Column(db.String(15), default='DRAFT')
    name_instance_id = db.Column('name_instance_id', db.BigInteger)
    name_id = db.Column('name_id', db.BigInteger, primary_key=True)

    nr_num = db.Column('nr_num', db.String(10), db.ForeignKey('bc_registries_names.request_submission_info.nr_num'))
    nro_name_request = db.relationship('NRORequestSubmission')

    def json(self):
        return {"name": self.name, "choice": self.choice, "state": self.state}

