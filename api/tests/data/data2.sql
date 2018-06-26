
insert into requests
(id,last_update,state_cd,nr_num,consent_flag,request_id,request_type_cd,priority_cd,xpro_jurisdiction,additional_info,
nature_business_info,user_id,furnished,expiration_date,previous_request_id,submit_count,submitted_date,submitter_userid)
values
(nextval('requests_id_seq'), '2018-04-02 20:09:03.626463', 'DRAFT', 'NR 0000022', null, null, 'CR', 'Y', null, null,
'toothpick maker', 1, 'N',null, null, null, current_timestamp, null)
;

insert into names
(id,name,state,choice,consumption_date,remote_name_id,nr_id)
values( nextval('names_id_seq'), 'my good company', 'NE', 1, null, null, (select id from requests where nr_num='NR 0000022'))
;
insert into names
(id,name,state,choice,consumption_date,remote_name_id,nr_id)
values( nextval('names_id_seq'), 'my better company', 'NE', 2, null, null, (select id from requests where nr_num='NR 0000022'))
;
insert into names
(id,name,state,choice,consumption_date,remote_name_id,nr_id)
values( nextval('names_id_seq'), 'my best company', 'NE', 3, null, null, (select id from requests where nr_num='NR 0000022'))
;


insert into applicants
(party_id,last_name,first_name,middle_name,phone_number,fax_number,email_address,contact,client_first_name,client_last_name,decline_notification_ind,addr_line_1,addr_line_2,addr_line_3,city,postal_cd,state_province_cd,country_type_cd,nr_id)
values
(nextval('applicants_party_id_seq'),'last_name','first_name','middle_name','phone_number','fax_number','email_address','contact','client_first_name','client_last_name','N','addr_line_1','addr_line_2','addr_line_3','city','postal_cd','BC','CA',
(select id from requests where nr_num='NR 0000022'))
;



insert into comments
(id,comment,user_id,nr_id)
values
(nextval('comments_id_seq'),'throwing shade in the playground',1,
(select id from requests where nr_num='NR 0000022'))
;

insert into comments
(id,comment,user_id,nr_id)
values
(nextval('comments_id_seq'),'caught that go ref?',1,
(select id from requests where nr_num='NR 0000022'))
;

insert into partner_name_system (id, partner_name_type_cd, partner_name_number, partner_jurisdiction_type_cd,
partner_name_date,partner_name,nr_id)
values
(nextval('partner_name_system_id_seq'), 'A', '123456', 'AB',null,'Sponge Bob',
(select id from requests where nr_num='NR 0000022'))
;

insert into partner_name_system (id, partner_name_type_cd, partner_name_number, partner_jurisdiction_type_cd,
partner_name_date,partner_name,nr_id)
values
(nextval('partner_name_system_id_seq'), 'AS', '234567', 'SK',null,'Count Sponge Bob',
(select id from requests where nr_num='NR 0000022'))
;
