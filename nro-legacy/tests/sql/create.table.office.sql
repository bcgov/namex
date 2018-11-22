drop table if exists office;

create table office(
    corp_num            varchar(10),
    office_typ_cd       varchar(10),
    start_event_id      varchar(10),
    end_event_id        varchar(10),
    mailing_addr_id     varchar(10),
    delivery_addr_id    varchar(10),
    dd_corp_num         varchar(10),
    email_address       varchar(10)
);