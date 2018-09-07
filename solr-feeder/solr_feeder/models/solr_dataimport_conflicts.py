
from . import base_schema, db


# The class that corresponds to the database view for conflicts core dataimports.
class SolrDataimportConflicts(db.Model):
    __bind_key__ = 'bc_registries_names_fdw'
    __table_args__ = {'schema': 'bc_registries_names'}
    __tablename__ = 'solr_dataimport_conflicts_vw'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    state_type_cd = db.Column(db.String)
    source = db.Column(db.String)

    @classmethod
    def find(cls, find_id):
        return cls.query.filter_by(id=find_id).one_or_none()


# The corresponding marshmallow-based schema used for serialization to JSON.
class SolrDataimportConflictsSchema(base_schema.BaseSchema):
    class Meta:
        model = SolrDataimportConflicts
