drop table if exists corp_name;

create table corp_name(
  corp_num    varchar(10),
  start_event_id varchar(10),
  end_event_id  varchar(10),
  corp_name_typ_cd  varchar(10),
  corp_nme varchar(100)
);