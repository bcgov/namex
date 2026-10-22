from . import db, ma


class NRNumberExclude(db.Model):
    __tablename__ = 'nr_number_exclude'
    nr_num = db.Column(db.String(10), primary_key=True)

    @classmethod
    def check_nr_num_exclude(cls, nr_num):
        return db.session.query(db.exists().where(cls.nr_num == nr_num)).scalar()

    def json(self):
        return {'nr_num': self.nr_num}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class NRNumberExcludeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = NRNumberExclude
