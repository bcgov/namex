create or replace PROCEDURE SYNC_CONSUMED_NAMES 

IS

   name_row name_instance%ROWTYPE;
   rs_row  request_state%ROWTYPE;
   r_row request%ROWTYPE;
   c_row corporation@colin_readonly%ROWTYPE;
   cname_row corp_name@colin_readonly%ROWTYPE;
   consumed_row name_instance%ROWTYPE;
  

   last_nr_num  VARCHAR2(10);
   r_nr_num VARCHAR2(10);
   next_request_id REQUEST.REQUEST_ID%TYPE;
   r_request_id REQUEST.REQUEST_ID%TYPE;
   request_type_var REQUEST_INSTANCE.REQUEST_TYPE_CD%TYPE;
   name_id NAME.NAME_ID%TYPE;
   eid event.event_id%TYPE;
   l_msg APPLICATION_LOG.LOG_MESSAGE%TYPE;
   jurisdiction_var REQUEST_INSTANCE.XPRO_JURISDICTION%TYPE;
   txn_count NUMBER;
   ni_count NUMBER;
   filing_count NUMBER;
   r_count NUMBER;
   skip_count NUMBER;
   counter NUMBER;
   max_count NUMBER;


   -- name consumption started going over to Namex on May 10th, 2019 was the first consumption in prod
   cursor ld_cursor is
   
    SELECT * from namex.solr_dataimport_conflicts_vw@colin_readonly 
    WHERE TRUNC(start_date)  <  to_date('20190510','YYYYMMDD') and id not in (select corp_num from namex_datafix) 
    ORDER BY id;
       
  
BEGIN
max_count := 10000;
counter := 0;

FOR cur_row IN ld_cursor loop

    SELECT count(c.corp_num) INTO skip_count 
      FROM corp_name@colin_readonly c
      LEFT OUTER JOIN namex.solr_dataimport_conflicts_vw@colin_readonly  solr ON solr.id = c.corp_num
      WHERE c.corp_num = cur_row.id and c.end_event_id is null 
        AND ((c.corp_name_typ_cd = 'NB' )
        OR (solr.jurisdiction='FD' and c.corp_name_typ_cd='CO'));
        
     IF skip_count > 0 THEN 
         l_msg := 'Skipped because it is a numbered company for FD jurisdiction';
         last_nr_num := '';
   		 GOTO track;
	 END IF;
      
       
       /*  GET THE REST OF THE SET UP DATA  */
	  --get an eventID for all new rows
		  SELECT event_seq.NEXTVAL  INTO eid  FROM dual;
		  INSERT INTO event (event_id, event_type_cd, event_timestamp)
          VALUES (eid, 'SYST', sysdate);
          

          --CURSOR RETURNS BC for BC jursidictionins5ead of BLANK-normalize data				  
		  If cur_row.jurisdiction = 'BC' THEN 
		      jurisdiction_var := NULL;
          ELSE
             jurisdiction_var := cur_row.jurisdiction;
          END IF;

          --get the corp_type not supplied in the cursor for the current corp
  	     SELECT * INTO c_row FROM corporation@colin_readonly where corp_num = cur_row.id;

		  --look for NR filing in CPRD and get the most recent one
               
         -- base nr on filing. effective
         
         SELECT count(f.nr_num) INTO filing_count
         FROM filing@colin_readonly f
		  INNER JOIN event@colin_readonly e ON e.event_id = f.event_id
		  WHERE f.nr_num is not null and e.corp_num = cur_row.id 
            and f.effective_dt = (SELECT MAX(f1.effective_dt)
                                    FROM filing@colin_readonly f1
		                           INNER JOIN event@colin_readonly e1 ON e1.event_id = f1.event_id
                                    WHERE f1.nr_num is not null and e1.corp_num = cur_row.id);
              
          If filing_count > 0 THEN 
            SELECT f.nr_num INTO last_nr_num 
		    FROM filing@colin_readonly f
		    INNER JOIN event@colin_readonly e ON e.event_id = f.event_id
		    WHERE f.nr_num is not null and e.corp_num = cur_row.id
            and f.effective_dt = (SELECT MAX(f1.effective_dt)
                                    FROM filing@colin_readonly f1
		                           INNER JOIN event@colin_readonly e1 ON e1.event_id = f1.event_id
                                    WHERE f1.nr_num is not null and e1.corp_num = cur_row.id);
		  END IF;        
   
         /* END OF THE SET UP DATA */

        --NO NR EXISTS IN THE CPRD FILING TABLE
        IF filing_count = 0 THEN

           --check to see if name has already been consumed for the current corp_num
           SELECT count(ni.corp_num) INTO ni_count
            FROM name_instance ni
            WHERE ni.end_event_id IS NULL 
              and ni.corp_num = cur_row.id;
           
           IF ni_count > 1 THEN 
              l_msg := 'NR # does not exist in CPRD filing table and Names but has duplicate NAME INSTANCE rows. ';
              GOTO track;
           END IF;
           
           IF ni_count = 1 THEN

            -- NAME exists in NAMES, clean up messy consumption
          
              SELECT ni.* INTO consumed_row
               FROM name_instance ni
               WHERE ni.end_event_id IS NULL 
                  and ni.corp_num = cur_row.id;
                         
              IF consumed_row.consumption_date IS NULL THEN 
                 UPDATE name_instance
                 SET consumption_date = cur_row.start_date
                 WHERE name_instance_id = consumed_row.name_instance_id;
              END IF;
              
               --get the NR #, request info
               SELECT r.request_id, r.nr_num INTO r_request_id, r_nr_num
               FROM request r
               LEFT OUTER JOIN name n ON r.request_id = n.request_id
               WHERE n.name_id = consumed_row.name_id ;
            
              SELECT rs.* INTO rs_row
              FROM request_state rs
              WHERE rs.request_id = r_request_id and rs.end_event_id IS NULL;
            
              IF rs_row.state_type_cd != 'COMPLETED' THEN
              
                  UPDATE request_state
                  SET end_event_id = eid
                  WHERE request_state_id = rs_row.request_state_id;
                 
                 -- add a clean completed state
                   INSERT INTO request_state
                   (request_state_id, request_id, state_type_cd, start_event_id, examiner_idir, examiner_comment)
		           VALUES
		           (request_state_seq.nextval, r_request_id, 'COMPLETED', eid, 'FIX_NR', 'ADDED MISSING COMPLETION state for CORP');
                          
              END IF;
             
              SELECT count(t.transaction_id)  INTO txn_count
              FROM transaction t
              WHERE request_id = r_request_id and t.transaction_type_cd = 'CONSUME';
              IF txn_count = 0 THEN
                    --trigger the extractor and complete consumption record set
		           INSERT INTO transaction 
		           (transaction_id, transaction_type_cd, event_id, request_id, staff_idir)
		            VALUES
                   (transaction_seq.nextval, 'CONSUME', eid, r_request_id, 'FIX_NR');
                   
                   l_msg := 'Added Transaction CONSUME';
              END IF;
          
             last_nr_num := r_nr_num;
             GOTO track;
          END IF; --ni_count != 1

           --Otherwise, NO NR EXISTS IN CPRD FILING TABLE OR NAMESP, CREATE A NEW NR IN NAMES
          SELECT request_seq.nextval INTO next_request_id FROM dual;

            --generate a new NR #
		   SELECT nro_util_pkg.get_new_nr_num() INTO last_nr_num FROM dual;

             l_msg := 'NEW NR';

            --get the request type.
            CASE 
               WHEN c_row.corp_typ_cd IN ('BC','QA','QB','QC','QD','QE','C') THEN request_type_var := 'CR';
               WHEN c_row.corp_typ_cd='ULC' THEN request_type_var := 'UL';
               WHEN c_row.corp_typ_cd IN ('S','CS') THEN request_type_var := 'SO';
               WHEN c_row.corp_typ_cd in ('A', 'B', 'EPR', 'FOR', 'REG') THEN request_type_var := 'XCR';
               WHEN c_row.corp_typ_cd='B' THEN request_type_var := 'XCR';
               WHEN c_row.corp_typ_cd='XS' THEN request_type_var := 'XSO';
               WHEN c_row.corp_typ_cd='ULC' THEN request_type_var := 'UL';
               WHEN c_row.corp_typ_cd='LLC' THEN request_type_var := 'LC';
             ELSE
               request_type_var := c_row.corp_typ_cd;
             END CASE;

		     INSERT INTO request
		     (request_id, nr_num, submit_count)
		     VALUES
		     (next_request_id, last_nr_num, 1);

              --get the request type.
             CASE 
               WHEN c_row.corp_typ_cd IN ('BC','QA','QB','QC','QD','QE','C') THEN request_type_var := 'CR';
               WHEN c_row.corp_typ_cd='ULC' THEN request_type_var := 'UL';
               WHEN c_row.corp_typ_cd IN ('S','CS')THEN request_type_var := 'SO';
               WHEN c_row.corp_typ_cd in ('A', 'B', 'EPR', 'FOR', 'REG') THEN request_type_var := 'XCR';
               WHEN c_row.corp_typ_cd='B' THEN request_type_var := 'XCR';
               WHEN c_row.corp_typ_cd='XS' THEN request_type_var := 'XSO';
               WHEN c_row.corp_typ_cd='ULC' THEN request_type_var := 'UL';
               WHEN c_row.corp_typ_cd='LLC' THEN request_type_var := 'LC';
             ELSE
               request_type_var := c_row.corp_typ_cd;
             END CASE;

		     INSERT INTO request_instance
		     (request_instance_id, request_id, request_type_cd, start_event_id, xpro_jurisdiction, nature_Business_info, admin_comment)
		     VALUES
		     (request_instance_seq.nextval,next_request_id, request_type_var, eid, jurisdiction_var, 'Added Missing NR for Active Corp.','NEW NR');

		     INSERT INTO request_state
		     (request_state_id, request_id, state_type_cd, start_event_id, examiner_idir, examiner_comment)
		     VALUES
		     (request_state_seq.nextval, next_request_id, 'COMPLETED', eid, 'FIX_NR', 'ADDED MISSING NR FOR ACTIVE CORP');


		     SELECT name_seq.nextval INTO name_id FROM dual;

		     INSERT INTO name
		     (name_id, request_id)
		     VALUES
		     (name_id, next_request_id);

		     --add a clean consumption row
		     INSERT INTO name_instance
		     (name_instance_id, name_id, choice_number, name,  search_name, consumption_date, start_event_id, corp_num)
		     VALUES
		     (name_instance_seq.nextval, name_id, 1, cur_row.name,  REPLACE(cur_row.name,' ',''),cur_row.start_date, eid,cur_row.id );

		     --add approved name state
		    INSERT INTO name_state
		    (name_state_id, name_id, name_state_type_cd, start_event_id)
		    VALUES
		    (name_state_seq.nextval, name_id, 'A', eid );

		    --trigger the extractor and complete consumption record set
		    INSERT INTO transaction 
		    (transaction_id, transaction_type_cd, event_id, request_id, staff_idir)
		    VALUES
		    (transaction_seq.nextval, 'CONSUME', eid, next_request_id, 'FIX_NR');
            
            l_msg := 'Does not exist in the filing table and does not exit in names';
            GOTO track;

	ELSE  -- NR_NUM IN FILING
          
            --compress the NR to get rid of formattig issues.
            last_nr_num := REPLACE(last_nr_num, ' ', '');
            
            SELECT count(request_id) INTO r_count
            FROM request  WHERE REPLACE(nr_num,' ','') = last_nr_num;
             /*THE NR EXISTS IN CPRD FILING TABLE and finds it in NAMESP*/
            IF r_count > 0 THEN
               SELECT * INTO r_row
               FROM request  WHERE REPLACE(nr_num,' ','') = last_nr_num;
               --get the current state to ensure that it is correct for consumption
		       SELECT * INTO rs_row FROM request_state WHERE request_id = r_row.request_id and end_event_id IS NULL;
             
               IF rs_row.state_type_cd != 'COMPLETED' THEN 
                    UPDATE request_state
			  	    SET end_event_id = eid
				    WHERE request_id = rs_row.request_id AND end_event_id is NULL;

				    INSERT INTO request_state
				    (request_state_id, request_id, state_type_cd, start_event_id, examiner_idir, examiner_comment)
				    VALUES
				    (request_state_seq.nextval, rs_row.request_id, 'COMPLETED', eid, 'FIX_NR', 'ADDED MISSING COMPLETION FOR CLEAN CONSUMPTION');
                END IF;

                --ensure there is an approved name row  
                SELECT count(ni.name_instance_id) INTO ni_count
                FROM name n
                LEFT OUTER JOIN name_instance ni on ni.name_id = n.name_id
		        LEFT OUTER JOIN name_state ns on ns.name_id = n.name_id
		        WHERE  n.request_id = r_row.request_id 
		           and ns.name_state_type_cd in ('A','C') 
		           and ni.end_event_id is null 
			       and ns.end_event_id IS NULL;
                   
               IF ni_count > 1 THEN 
                  l_msg := 'NR # does not exist in CPRD filing table and Names but has duplicate NAME INSTANCE rows. ';
                  GOTO track;
                END IF;  
               
               IF ni_count = 1 THEN
                
		         SELECT ni.* into name_row 
                 FROM name n
		         LEFT OUTER JOIN name_instance ni on ni.name_id = n.name_id
		         LEFT OUTER JOIN name_state ns on ns.name_id = n.name_id
		         WHERE  n.request_id = r_row.request_id 
		            and ns.name_state_type_cd in ('A','C') 
		            and ni.end_event_id is null 
			        and ns.end_event_id IS NULL;

                 --THE NR IS THE CORRECT STATE, CHECK THE CONSUMPTION and UPDATE IF IT IS MISSING DATA
		         IF (name_row.consumption_date IS NULL  OR  name_row.corp_num IS NULL) THEN 
             	    --end the current name instance
		            UPDATE name_instance
			        SET end_event_id = eid
			        WHERE name_instance_id = name_row.name_instance_id;

			        --add a clean consumption row
			        INSERT INTO name_instance
			        (name_instance_id, name_id, choice_number, name, designation, consumption_date, search_name, start_event_id, corp_num)
			        VALUES
			       (name_instance_seq.nextval, name_row.name_id, name_row.choice_number, name_row.name,name_row.designation, cur_row.start_date, name_row.search_name, eid,cur_row.id );
                  END IF;
                 
                  SELECT count(t.transaction_id) INTO txn_count
                  FROM transaction t
                  WHERE request_id = r_request_id and t.transaction_type_cd = 'CONSUME';
                  IF txn_count = 0 THEN
                      --trigger the extractor and complete consumption record set
		             INSERT INTO transaction 
		             (transaction_id, transaction_type_cd, event_id, request_id, staff_idir)
		              VALUES
                     (transaction_seq.nextval, 'CONSUME', eid, r_row.request_id, 'FIX_NR');
                   
                     l_msg := 'Added Transaction CONSUME, Exist in Filing and Names';
                  END IF;
                
              ELSE --ni_count !=1

                   l_msg := 'NR # exists in CPRD filing table and Names but does not exist in NAME INSTANCE or NAME STATE. Check--ensure there is an approved name row ';
        	  END IF;


		  ELSE --r_count !> 0  means that CPRD filing table has an NR that does not exist in Names
               -- USing the existing NR that came from CPRD - to match it.
			  --the NR does not exist in names, add all necessary table/rows for it to be consumed
			  select request_seq.nextval INTO next_request_id FROM dual;
              
              --make sure NR format is correct for Names
              IF SUBSTR(last_nr_num,3,1) != ' ' THEN 
                 last_nr_num := REPLACE(last_nr_num,'NR', 'NR ');
              END IF;

			  INSERT INTO request
			  (request_id, nr_num, submit_count)
			  VALUES
			  (next_request_id, last_nr_num, 1);
            --determine request_type
             CASE 
               WHEN c_row.corp_typ_cd IN ('BC','QA','QB','QC','QD','QE', 'C') THEN request_type_var := 'CR';
               WHEN c_row.corp_typ_cd='ULC' THEN request_type_var := 'UL';
               WHEN c_row.corp_typ_cd IN ('S','CS') THEN request_type_var := 'SO';
               WHEN c_row.corp_typ_cd in ('A', 'B', 'EPR', 'FOR', 'REG') THEN request_type_var := 'XCR';
               WHEN c_row.corp_typ_cd='B' THEN request_type_var := 'XCR';
               WHEN c_row.corp_typ_cd='XS' THEN request_type_var := 'XSO';
               WHEN c_row.corp_typ_cd='ULC' THEN request_type_var := 'UL';
               WHEN c_row.corp_typ_cd='LLC' THEN request_type_var := 'LC';
             ELSE
               request_type_var := c_row.corp_typ_cd;
             END CASE;

			  INSERT INTO request_instance
			  (request_instance_id, request_id, request_type_cd, start_event_id, xpro_jurisdiction, nature_Business_info, admin_comment)
			  VALUES
			  (request_instance_seq.nextval,next_request_id, request_type_var, eid, jurisdiction_var, 'Added Missing NR for Active Corp','Datafix for conflict matching');

			  INSERT INTO request_state
			  (request_state_id, request_id, state_type_cd, start_event_id, examiner_idir, examiner_comment )
			  VALUES
			  (request_state_seq.nextval, next_request_id, 'COMPLETED', eid, 'FIX_NR', 'ADDED MISSING COMPLETION FOR CLEAN CONSUMPTION');

			  SELECT name_seq.nextval INTO name_id FROM dual;

			  INSERT INTO name
			  (name_id, request_id)
			  VALUES
			  (name_id, next_request_id);

			  --add a clean consumption row
			  INSERT INTO name_instance
			  (name_instance_id, name_id, choice_number, name,  search_name, consumption_date, start_event_id, corp_num)
			  VALUES
			  (name_instance_seq.nextval, name_id, 1, cur_row.name, REPLACE(cur_row.name,' ',''),cur_row.start_date, eid,cur_row.id );

			  --add approved name state
			  INSERT INTO name_state
			  (name_state_id, name_id, name_state_type_cd, start_event_id)
			  VALUES
			  (name_state_seq.nextval, name_id, 'A', eid );

			  --trigger the extractor and complete consumption
			  INSERT INTO transaction 
			  (transaction_id, transaction_type_cd, event_id, request_id, staff_idir)
			  values
			  (transaction_seq.nextval, 'CONSUME', eid, next_request_id, 'FIX_NR');
                l_msg := 'Added Transaction CONSUME, Exist in Filing but does not exist Names';
		END IF; -- --r_row.request_id > 0

	END IF;	--last_nr_num IS NULL OR last_nr_num='' THEN

    <<track>>
    --keep track of errors and what the last one completed is
    INSERT INTO NAMEX_DATAFIX
    (id, nr_num, corp_num, msg)
    VALUES
    (namex_datafix_seq.nextval, last_nr_num, cur_row.id, l_msg);
    
    --DBMS_OUTPUT.PUT_LINE('Corp_num:'||cur_row.id); 

  COMMIT;
  counter := counter + 1;
  IF counter > max_count THEN
      DBMS_OUTPUT.PUT_LINE('Max rows met:'||counter); 
     EXIT;
  END IF;
END LOOP;
END SYNC_CONSUMED_NAMES;