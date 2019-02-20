from sqlalchemy import text
from datetime import datetime

import opentracing
from opentracing.ext import tags

tracer = opentracing.tracer


class JobTracker(object):

    @staticmethod
    def start_job(db, start_time):
        parent_span = tracer.active_span
        with tracer.start_active_span('start_job', child_of=parent_span) as scope:
            state = 'running'
            sql = text('insert into nro_names_sync_job (status_cd, start_time) values (:state, :start_time) returning id')
            scope.span.set_tag(tags.DATABASE_TYPE, 'postgresql')
            scope.span.set_tag(tags.DATABASE_STATEMENT, sql)
            scope.span.set_tag('db.statement.parameters', "{}, {}".format(state, start_time))

            result = db.engine.execute(sql.params(state=state, start_time=start_time))
            row = result.fetchone()
            scope.span.set_tag('db.answer', row)
            id = int(row['id'])

            return id

    @staticmethod
    def job_detail(db, job_id, nr_num):
        parent_span = tracer.active_span
        with tracer.start_active_span('start_job', child_of=parent_span) as scope:
            sql = text('insert into nro_names_sync_job_detail (job_id, nr_num, time, success) values (:job_id, :nr_num, :event_time, true)')
            scope.span.set_tag(tags.DATABASE_TYPE, 'postgresql')
            scope.span.set_tag(tags.DATABASE_STATEMENT, sql)
            scope.span.set_tag('db.statement.parameters', "{}, {}".format(job_id, nr_num))
            db.engine.execute(sql.params(job_id=job_id, nr_num=nr_num, event_time=datetime.utcnow()))

    @staticmethod
    def job_detail_error(db, job_id, nr_num, errMsg):
        parent_span = tracer.active_span
        with tracer.start_active_span('start_job', child_of=parent_span) as scope:
            sql = text('insert into nro_names_sync_job_detail (job_id, nr_num, time, success, error_msg) values (:job_id, :nr_num, :event_time, false, :errMsg)')
            scope.span.set_tag(tags.DATABASE_TYPE, 'postgresql')
            scope.span.set_tag(tags.DATABASE_STATEMENT, sql)
            scope.span.set_tag('db.statement.parameters', "{}, {}, {}".format(job_id, nr_num, errMsg))
            db.engine.execute(sql.params(job_id=job_id, nr_num=nr_num, event_time=datetime.utcnow(), errMsg=errMsg))

    @staticmethod
    def end_job(db, job_id, end_time, state):
        parent_span = tracer.active_span
        with tracer.start_active_span('start_job', child_of=parent_span) as scope:
            sql = text('update nro_names_sync_job set status_cd = :state, end_time = :end_time where id = :job_id')
            scope.span.set_tag(tags.DATABASE_TYPE, 'postgresql')
            scope.span.set_tag(tags.DATABASE_STATEMENT, sql)
            scope.span.set_tag('db.statement.parameters', "{}, {}, {}".format(job_id, state, end_time))
            db.engine.execute(sql.params(job_id=job_id, state=state, end_time=end_time))
