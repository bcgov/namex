from . import db
from datetime import datetime


class HotjarTracking(db.Model):
    __tablename__ = 'hotjar_tracking'

    id = db.Column(db.Integer, primary_key=True)
    hotjarUser = db.Column('hotjar_user', db.String(20))
    lastUpdate = db.Column(
        'last_update_dt', db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # parent keys
    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'), index=True)

    def as_dict(self):
        return {
            'id': self.id,
            'hotjarUser': self.hotjarUser,
            'nrId': self.nrId,
            'lastUpdate': self.lastUpdate.isoformat(),
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        pass
