
from . import base_schema, db


# The class that corresponds to the database view for names core dataimports.
class SolrDataimportNames(db.Model):
    __bind_key__ = 'bc_registries_names_fdw'
    __table_args__ = {'schema': 'bc_registries_names'}
    __tablename__ = 'solr_dataimport_names_vw'

    id = db.Column(db.String, primary_key=True)
    name_instance_id = db.Column(db.Integer)
    choice_number = db.Column(db.Integer)
    corp_num = db.Column(db.String)
    name = db.Column(db.String)
    nr_num = db.Column(db.String)
    request_id = db.Column(db.Integer)
    submit_count = db.Column(db.Integer)
    request_type_cd = db.Column(db.String)
    name_id = db.Column(db.Integer)
    start_event_id = db.Column(db.Integer)
    name_state_type_cd = db.Column(db.String)

    @classmethod
    def find(cls, nr_num) -> list:
        return cls.query.filter_by(nr_num=nr_num).all()


# The corresponding marshmallow-based schema used for serialization to JSON.
class SolrDataimportNamesSchema(base_schema.BaseSchema):
    class Meta:
        model = SolrDataimportNames
