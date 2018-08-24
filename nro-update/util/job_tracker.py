from sqlalchemy import text
from datetime import datetime


class JobTracker(object):

    @staticmethod
    def start_job(db, start_time):
        state = 'running'
        sql = text('insert into nro_names_sync_job (status_cd, start_time) values (:state, :start_time) returning id')

        result = db.engine.execute(sql.params(state=state, start_time=start_time))
        row = result.fetchone()
        id = int(row['id'])

        return id

    @staticmethod
    def job_detail(db, job_id, nr_num):
        sql = text('insert into nro_names_sync_job_detail (job_id, nr_num, time) values (:job_id, :nr_num, :event_time)')

        db.engine.execute(sql.params(job_id=job_id, nr_num=nr_num, event_time=datetime.utcnow()))

    @staticmethod
    def end_job(db, job_id, end_time, state):
        sql = text('update nro_names_sync_job set status_cd = :state, end_time = :end_time where id = :job_id')

        db.engine.execute(sql.params(job_id=job_id, state=state, end_time=end_time))
