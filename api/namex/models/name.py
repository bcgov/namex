"""Name hold a name choice for a Request
"""
# from . import db, ma
from marshmallow import fields
from sqlalchemy import event
from sqlalchemy.orm import backref
from sqlalchemy.orm.attributes import get_history

from namex.models import db, ma


class Name(db.Model):
    __tablename__ = 'names'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), index=True)
    state = db.Column(db.String(15), default='NE')  # NE=Not Examined; R=Rejected; A=Accepted; C=Cond. Accepted
    choice = db.Column(db.Integer)
    designation = db.Column(db.String(50), default=None)
    consumptionDate = db.Column('consumption_date', db.DateTime(timezone=True))
    corpNum = db.Column('corp_num', db.String(10), default=None)
    remoteNameId = db.Column('remote_name_id', db.BigInteger)

    # Decision info
    conflict1 = db.Column(db.String(250), default='')  # optional conflict name
    conflict2 = db.Column(db.String(250), default='')  # optional conflict name
    conflict3 = db.Column(db.String(250), default='')  # optional conflict name
    conflict1_num = db.Column(db.String(250), default='')  # optional conflict name - corp or NR number
    conflict2_num = db.Column(db.String(250), default='')  # optional conflict name - corp or NR number
    conflict3_num = db.Column(db.String(250), default='')  # optional conflict name - corp or NR number
    decision_text = db.Column(db.String(1000), default='')

    nrId = db.Column('nr_id', db.Integer, db.ForeignKey('requests.id'), index=True)
    commentId = db.Column('comment_id', db.Integer, db.ForeignKey('comments.id'))
    # nameRequest = db.relationship('Request')

    # if a comment is added during decision, link it to the name record to be sent back to NRO
    comment = db.relationship("Comment", backref=backref("related_name", uselist=False), foreign_keys=[commentId])

    # Required for name request name analysis
    _name_type_cd = db.Column('name_type_cd', db.String(10))

    NOT_EXAMINED = 'NE'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    CONDITION = 'CONDITION'
    # Needed for name request reservation before completing the nr
    RESERVED = 'RESERVED'
    COND_RESERVE = 'COND-RESERVE'

    # Properties added for Name Request
    @property
    def name_type_cd(self):
        """Property containing the name type which is used by name Request."""
        return self._name_type_cd

    @name_type_cd.setter
    def name_type_cd(self, value: str):
        self._name_type_cd = value

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'name_type_cd': self.name_type_cd,
            'designation': self.designation,
            'choice': self.choice,
            'state': self.state,
            'conflict1': self.conflict1,
            'conflict2': self.conflict2,
            'conflict3': self.conflict3,
            'conflict1_num': self.conflict1_num,
            'conflict2_num': self.conflict2_num,
            'conflict3_num': self.conflict3_num,
            'decision_text': self.decision_text,
            'consumptionDate': self.consumptionDate.isoformat() if self.consumptionDate else None,
            'corpNum': self.corpNum,
            'comment': None if self.comment is None else self.comment.as_dict()
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        # force uppercase names
        self.name = self.name.upper()

        db.session.add(self)
        db.session.commit()

    def add_to_db(self):
        db.session.add(self)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

@event.listens_for(Name, 'after_insert')
@event.listens_for(Name, 'after_update')
def update_nr_name_search(mapper, connection, target):
    """Add any changes to the name to the request.nameSearch column and publish name state changes where applicable."""
    from flask.globals import current_app
    
    from namex.models import Event, Request, State
    from namex.services.audit_trail.event_recorder import EventRecorder

    name = target
    nr = Request.find_by_id(name.nrId)
    if nr:
        # get the names associated with the NR
        names_q = connection.execute(
            f"""
            SELECT names.name from names
            JOIN requests on requests.id = names.nr_id
            WHERE requests.id={nr.id}
            """
        )
        # format the names into a string like: |1<name1>|2<name2>|3<name3>
        names = [x[0] for x in names_q.all()]
        name_search = ''
        for item, index in zip(names, range(len(names))):
            name_search += f'|{index + 1}{item}{index + 1}|'
        # update the name_search field of the nr with the formatted string
        connection.execute(
            """
            UPDATE requests
            SET name_search=%s
            WHERE id=%s
            """,
            ('(' + name_search + ')', nr.id)
        )

        # set nr state to consumed
        name_consume_history = get_history(name, 'corpNum')
        current_app.logger.debug('name_consume_history.added {}'.format(nr.nrNum))
        if len(name_consume_history.added):
            # Adding an after_flush_postexec to avoid connection and transaction closed issue's
            # Creating one time execution event when ever corpNum is added to a name
            # corpNum sets from nro-extractor job
            @event.listens_for(db.session, 'after_flush_postexec', once=True)
            def receive_after_flush_postexec(session, flush_context):
                nr = Request.find_by_id(name.nrId)
                nr.stateCd = State.CONSUMED
                nr.add_to_db()
                current_app.logger.debug('moved to CONSUMED state {}'.format(name.corpNum))
                EventRecorder.record_as_system(Event.UPDATE_FROM_NRO, nr, {
                    'id': nr.id,
                    'nrNum': nr.nrNum,
                    'stateCd': nr.stateCd
                }, True)
                current_app.logger.debug('moved to CONSUMED state event logged {}'.format(nr.nrNum))


class NameSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Name
        fields = (
            'choice',
            'comment',
            'conflict1',
            'conflict2',
            'conflict3',
            'conflict1_num',
            'conflict2_num',
            'conflict3_num',
            'consumptionDate',
            'corpNum',
            'decision_text',
            'designation',
            'id',
            'name_type_cd',
            'name',
            'state'
        )

    conflict1 = fields.String(required=False, allow_none=True)
    conflict2 = fields.String(required=False, allow_none=True)
    conflict3 = fields.String(required=False, allow_none=True)
    conflict1_num = fields.Field(required=False, allow_none=True)
    conflict2_num = fields.Field(required=False, allow_none=True)
    conflict3_num = fields.Field(required=False, allow_none=True)
    decision_text = fields.String(required=False, allow_none=True)
    comment = fields.String(required=False, allow_none=True)
    consumptionDate = fields.DateTime(required=False, allow_none=True)
    corpNum = fields.String(required=False, allow_none=True)
    designation = fields.String(required=False, allow_none=True)
    name = fields.String(
        required=True,
        error_messages={'required': {'message': 'name is a required field'}}
    )
    name_type_cd = fields.String(required=False, allow_none=True)
