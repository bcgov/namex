drop table if exists corp_op_state;

create table corp_op_state(
  state_typ_cd     varchar(10),
  op_state_typ_cd  varchar(10)
);