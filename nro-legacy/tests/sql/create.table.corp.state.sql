drop table if exists corp_state;

create table corp_state(
  corp_num          varchar(10),
  start_event_id    varchar(10),
  end_event_id      varchar(10),
  state_typ_cd      varchar(10)
);