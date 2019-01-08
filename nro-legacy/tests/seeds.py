from .postgres import Postgres


def seed_corp_name(corp_num, start_event_id, corp_name_typ_cd, corp_nme):
    Postgres().execute("""
           insert into corp_name(
                corp_num,
                start_event_id,
                end_event_id ,
                corp_name_typ_cd ,
                corp_nme
            )
        values ('{}','{}',null,'{}','{}')
     """.format(corp_num, start_event_id, corp_name_typ_cd, corp_nme))


def seed_corp_state(corp_num, start_event_id):
    Postgres().execute("""
            insert into corp_state(
                corp_num, 
                start_event_id,
                end_event_id,
                state_typ_cd
            )
        values ('{}', '{}',null,'ACT')
     """.format(corp_num, start_event_id))


def seed_corp(corp_num, corp_typ_cd):
    Postgres().execute("""
            insert into corporation(
                corp_num, 
                corp_typ_cd
            )
        values ('{}', '{}')
     """.format(corp_num, corp_typ_cd))


def seed_corp_type(corp_typ_cd, corp_class):
    Postgres().execute("""
            insert into corp_type(
                corp_typ_cd, 
                corp_class
            )
        values ('{}', '{}')
     """.format(corp_typ_cd, corp_class))

def seed_corp_op_state():
    Postgres().execute("""
            insert into corp_op_state(
            state_typ_cd,
            op_state_typ_cd
            )
        values('ACT', 'ACT')
        """)
