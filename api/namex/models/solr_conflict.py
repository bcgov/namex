from . import db, ma


class SolrConflict(db.Model):
    __tablename__ = 'solr_dataimport_conflicts_vw'

    id = db.Column(db.String(10), primary_key=True, autoincrement=False)
    name = db.Column('name', db.String(150), default='NONE', nullable=False, index=True)
    stateTypeCd = db.Column('state_type_cd', db.String(4), nullable=False, index=True)
    source = db.Column('source', db.String(4), nullable=False, index=True)
    startDate = db.Column('start_date', db.DateTime)
    jurisdiction = db.Column('jurisdiction', db.String(40), index=True)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "stateTypeCd": self.stateTypeCd,
            "source": self.source,
            "startDate": self.startDate,
            "jurisdiction": self.jurisdiction
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(name=name).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def save_to_session(self):
        db.session.add(self)


class SolrConflictSchema(ma.ModelSchema):
    class Meta:
        model = SolrConflict
