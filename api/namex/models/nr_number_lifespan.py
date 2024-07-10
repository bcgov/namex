from datetime import datetime, timedelta
from . import db, ma


class NRNumberLifespan(db.Model):
    __tablename__ = 'nr_number_lifespan'
    nr_num = db.Column(db.String(10), primary_key=True)
    nr_timestamp = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    @classmethod
    def check_nr_num_lifespan(cls, nr_num):
        return db.session.query(db.exists().where(cls.nr_num == nr_num)).scalar()

    @classmethod
    def insert_nr_num(cls, nr_num):
        entry = cls(nr_num=nr_num)
        db.session.add(entry)
        db.session.commit()

    @classmethod
    def delete_old_entries(cls, lifespan_seconds):
        expiration_time = datetime.utcnow() - timedelta(seconds=lifespan_seconds)
        db.session.query(cls).filter(cls.nr_timestamp < expiration_time).delete()
        db.session.commit()

    def json(self):
        return {'nr_num': self.nr_num, 'nr_timestamp': self.nr_timestamp}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class NRNumberLifespanSchema(ma.SQLAlchemySchema):
    class Meta:
        model = NRNumberLifespan
