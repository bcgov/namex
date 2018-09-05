
import marshmallow_sqlalchemy

from . import db


# The class that corresponds to the database view for completed name requests.
class CompletedNr(db.Model):
    __bind_key__ = 'bc_registries_names_fdw'
    __table_args__ = {'schema': 'bc_registries_names'}
    __tablename__ = 'completed_nr_vw'

    request_id = db.Column(db.Integer)
    nr_num = db.Column(db.String)
    submit_count = db.Column(db.Integer)
    request_instance_id = db.Column(db.Integer)
    request_type_cd = db.Column(db.String)
    name_id = db.Column(db.Integer)
    name_instance_id = db.Column(db.Integer, primary_key=True)
    choice_number = db.Column(db.Integer)
    name = db.Column(db.String)
    start_event_id = db.Column(db.Integer)
    corp_num = db.Column(db.String)
    name_state_type_cd = db.Column(db.String)
    expiration_date = db.Column(db.Date)
    consumption_date = db.Column(db.Date)

    @classmethod
    def find(cls, nr_num) -> list:
        return cls.query.filter_by(nr_num=nr_num).all()


# The corresponding marshmallow-based schema used for serialization to JSON.
class CompletedNrSchema(marshmallow_sqlalchemy.ModelSchema):
    class Meta:
        model = CompletedNr
