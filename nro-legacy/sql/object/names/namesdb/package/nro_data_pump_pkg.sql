CREATE OR PACKAGE nro_datapump_pkg AS


  --
  --
  PROCEDURE update_request_state(nr_number IN VARCHAR2,
				 status IN VARCHAR2,
				 expiry_date IN VARCHAR2,
				 consent_flag IN VARCHAR2,
				 examiner_id IN VARCHAR2,
				 exam_comment IN VARCHAR2 DEFAULT NULL,
				 add_info IN VARCHAR2 DEFAULT NULL,
				 p_corp_num IN VARCHAR2 DEFAULT NULL);

  --
  --
  PROCEDURE update_name_state(nr_number IN VARCHAR2,
			      name_choice IN VARCHAR2,
			      accept_reject_flag IN VARCHAR2,
			      reject_condition IN VARCHAR2 DEFAULT NULL);


  PROCEDURE update_name_rule(nr_number IN VARCHAR2,
			     name_choice IN VARCHAR2,
			     conflicting_number IN VARCHAR2,
			     conflicting_name IN VARCHAR2 DEFAULT NULL);

  PROCEDURE make_historical(p_corp_num IN VARCHAR2,
			    p_corp_type IN VARCHAR2,
			    p_corp_name IN VARCHAR2 DEFAULT NULL);

  PROCEDURE consume_request(p_nr_num IN VARCHAR2,
			    p_corp_num IN VARCHAR2);

  PROCEDURE name_examination(p_nr_number IN VARCHAR2,
			     p_status IN VARCHAR2,
			     p_expiry_date IN VARCHAR2,
			     p_consent_flag IN VARCHAR2,
			     p_examiner_id IN VARCHAR2,
			     p_choice1 IN VARCHAR2 DEFAULT 'NE',
			     p_choice2 IN VARCHAR2 DEFAULT 'NA',
			     p_choice3 IN VARCHAR2 DEFAULT 'NA',
			     p_exam_comment IN VARCHAR2 DEFAULT NULL,
			     p_add_info IN VARCHAR2 DEFAULT NULL,
			     p_confname1A IN VARCHAR2 DEFAULT 'NA',
			     p_confname1B IN VARCHAR2 DEFAULT 'NA',
			     p_confname1C IN VARCHAR2 DEFAULT 'NA',
			     p_confname2A IN VARCHAR2 DEFAULT 'NA',
			     p_confname2B IN VARCHAR2 DEFAULT 'NA',
			     p_confname2C IN VARCHAR2 DEFAULT 'NA',
			     p_confname3A IN VARCHAR2 DEFAULT 'NA',
			     p_confname3B IN VARCHAR2 DEFAULT 'NA',
			     p_confname3C IN VARCHAR2 DEFAULT 'NA');

  FUNCTION format_corp_num(p_corp_num IN VARCHAR2) RETURN name_instance.corp_num%TYPE;

  FUNCTION Dummy RETURN VARCHAR2;

END nro_datapump_pkg;