create or replace PACKAGE BODY nro_datapump_pkg AS

  RESTORATION_TYPES CONSTANT VARCHAR2(100) := ' RCR RCP RFI RLC XRCP XRSO RSO XRUL RUL XRCR ';

--
-- Convenience procedure for writing out information
-- in the session. The write statement is commented out
-- when not unit testing/troubleshooting.
--
PROCEDURE log_debug(p_message IN VARCHAR2) IS
  message_var VARCHAR2(256);

BEGIN
  message_var := substr(p_message, 1, 250);
  --dbms_output.put_line(message_var);
END;


   /*
   **
   ** FUNCTION format_corp_num
   **
   ** PURPOSE: Convert A, BC, C, CUL, ULC prefixed NAMES formatted company
   **          numbers to Colin formatted company numbers.
   **
   ** COMMENTS:
   **  Called by consume_request to update the request name_instance.corp_num
   **  column with a colin - formatted value, so that a later colin make historical
   **  process will match on the colin company number.
   **
   */
  FUNCTION format_corp_num(p_corp_num IN VARCHAR2) RETURN name_instance.corp_num%TYPE IS
    l_message APPLICATION_LOG.LOG_MESSAGE%TYPE;
    l_unit_name VARCHAR2(100);

    l_corp_num name_instance.corp_num%TYPE;
    l_corp_type VARCHAR2(3);

  BEGIN
    l_unit_name := 'get_colin_corp_num';
    l_message := 'Received corp_num: ' || p_corp_num;
    l_corp_num := p_corp_num;
--    dbms_output.put_line(l_message);

    IF (LENGTH(TRIM(l_corp_num)) > 3) THEN
      l_corp_type := SUBSTR(l_corp_num, 1, 3);
      l_message :=  l_message || ' derived corp_type= ' || l_corp_type;
--    dbms_output.put_line(l_message);
      IF (l_corp_type = 'BC ' OR l_corp_type = 'ULC') THEN
        l_corp_num := SUBSTR(l_corp_num, 4);
      ELSIF (l_corp_type = 'CUL' OR l_corp_type = 'C  ') THEN
        l_corp_num := 'C' || SUBSTR(l_corp_num, 4);
      ELSIF (l_corp_type = 'A  ') THEN
        l_corp_num := 'A' || SUBSTR(l_corp_num, 4);
      END IF;

    END IF;
    l_message := 'Returning colin formatted company number ' || l_corp_num;
--    dbms_output.put_line(l_message);

    RETURN l_corp_num;
  EXCEPTION
    WHEN OTHERS THEN
      application_log_insert('nro_datapump_pkg', SYSDATE, 1, string_limit( 'Exception in ' ||
                             l_unit_name || '; ' || l_message || '; SQLERRM: ' || SQLERRM, 4000));
      ROLLBACK;
  END;
 


/*
**
** PROCEDURE get_event
**
** PURPOSE: Create a new datapump event record and return the event_id.
**
** COMMENTS:
**
**
*/
  FUNCTION get_event(p_event_type IN event.event_type_cd%TYPE DEFAULT 'SYST') RETURN event.event_id%TYPE IS
    l_event_id event.event_id%TYPE;
    l_unit_name VARCHAR2(40);
    l_message VARCHAR2(256);
    l_event_type event.event_type_cd%TYPE;
  BEGIN
    l_unit_name := 'get_event';
    l_event_type := p_event_type;
    IF (l_event_type IS NULL OR LENGTH(TRIM(l_event_type)) < 1) THEN
      l_event_type := 'SYST';
    END IF;
    l_message := l_unit_name || ' getting event_id from sequence for event_type ' || p_event_type;
    log_debug(l_message);
    SELECT event_seq.NEXTVAL
      INTO l_event_id
      FROM dual;

    l_message := l_unit_name || ' Inserting into event with event_id ' || l_event_id;
    log_debug(l_message);
    INSERT INTO event (event_id, event_type_cd, event_timestamp)
      VALUES (l_event_id, l_event_type, sysdate);
    RETURN l_event_id;
  EXCEPTION
    WHEN OTHERS THEN
      application_log_insert('nro_datapump_pkg', SYSDATE, 1, string_limit( 'Exception in ' ||
                             l_message || '; SQLERRM: ' || SQLERRM, 4000));
      ROLLBACK;
  END;


/*
**
** PROCEDURE update_state
**
** PURPOSE:  Perform a logical update of the request_state
**           table using the provided parameter values.
**
** COMMENTS:
**
**
*/
  PROCEDURE update_state(p_request_id IN request.request_id%TYPE,
                         p_event_id IN event.event_id%TYPE,
                         p_state_code IN request_state.state_type_cd%TYPE,
                         p_examiner_id IN VARCHAR2 DEFAULT NULL,
                         p_examiner_comment IN VARCHAR2 DEFAULT NULL) IS
    l_unit_name VARCHAR2(40);
    l_message VARCHAR2(256);
  BEGIN
    l_unit_name := 'update_state';
    l_message := l_unit_name || ' updating request_state.end_event_id for request id ' || p_request_id;
    log_debug(l_message);
    UPDATE request_state rs
       SET rs.end_event_id = p_event_id
     WHERE rs.request_id = p_request_id
       AND rs.end_event_id IS NULL;

    l_message := l_unit_name || ' inserting into request_state for request_id=' || p_request_id || ' state=' || p_state_code;
    log_debug(l_message);
    INSERT INTO request_state (request_state_id, request_id, state_type_cd,
                               start_event_id, examiner_idir, examiner_comment)
         VALUES (request_state_seq.NEXTVAL, p_request_id, p_state_code, p_event_id, p_examiner_id, p_examiner_comment);

  EXCEPTION
    WHEN OTHERS THEN
      log_debug(l_message || '  FAILED');
      application_log_insert('nro_datapump_pkg', SYSDATE, 1, string_limit( 'Exception in ' ||
                             l_message || '; SQLERRM: ' || SQLERRM, 4000));
      ROLLBACK;
  END;


/*
**
** PROCEDURE get_assumed_request_type
**
** PURPOSE: For assumed name requests, get previous request type
**
** COMMENTS:
**
**
*/
  FUNCTION get_assumed_request_type(p_request_id request.request_id%TYPE) RETURN request_instance.request_type_cd%TYPE IS
    l_message APPLICATION_LOG.LOG_MESSAGE%TYPE;
    l_unit_name VARCHAR2(100);

    prev_request_id_var request.previous_request_id%TYPE;
    rec_type_var request_instance.request_type_cd%TYPE := '';
  BEGIN
    l_unit_name := 'get_assumed_request_type';
    l_message := 'Getting previous request id for request_id ' || p_request_id;
    dbms_output.put_line(l_message);

    SELECT r.previous_request_id
      INTO prev_request_id_var
      FROM request r
     WHERE r.request_id = p_request_id;

    l_message := 'Looking up previous request_type for previous_request_id ' || prev_request_id_var;
    dbms_output.put_line(l_message);

    BEGIN
       SELECT ri.request_type_cd
         INTO rec_type_var
         FROM request r, request_instance ri
        WHERE r.request_id = prev_request_id_var
          AND ri.request_id = r.request_id
          AND ri.end_event_id IS NULL;
    EXCEPTION
      WHEN OTHERS THEN
        rec_type_var := '';
    END;

    RETURN rec_type_var;
  EXCEPTION
    WHEN OTHERS THEN
      application_log_insert('nro_datapump_pkg', SYSDATE, 1, string_limit( 'Exception in ' ||
                             l_unit_name || '; ' || l_message || '; SQLERRM: ' || SQLERRM, 4000));
  END;


/*
**
** PROCEDURE cancel_resubmit
**
** PURPOSE: Set state of previous request to cancelled after a
**          resubmitted request has been processed.
**
** COMMENTS:
** Looks up RESUBMIT request. If present and previous request id exists,
** checks the state of the previous request.
**
**
*/
  PROCEDURE cancel_resubmit(p_request_id request.request_id%TYPE,
                            p_event_id event.event_id%TYPE) IS
    l_message APPLICATION_LOG.LOG_MESSAGE%TYPE;
    l_unit_name VARCHAR2(100);

    resubmit_count_var INTEGER := 0;
    previous_request_var request.previous_request_id%TYPE := 0;
    state_type_var request_state.state_type_cd%TYPE;
    state_id_var request_state.request_state_id%TYPE;
    event_id_var event.event_id%TYPE;
  BEGIN
    l_unit_name := 'cancel_resubmit';

    l_message := 'Counting resubmit requests for ' || p_request_id;
--    dbms_output.put_line('Counting resubmit requests for ' || p_request_id);
    SELECT COUNT(t.transaction_id)
      INTO resubmit_count_var
      FROM transaction t
     WHERE t.request_id = p_request_id
       AND t.transaction_type_cd = 'RESUBMIT';

--    dbms_output.put_line('Resubmit count=' || resubmit_count_var);
    IF (resubmit_count_var < 1) THEN
      RETURN;
    END IF;

    l_message := 'Getting previous request ID for ' || p_request_id;
--    dbms_output.put_line('Getting previous request ID for ' || p_request_id);
    SELECT r.previous_request_id
      INTO previous_request_var
      FROM request r
     WHERE r.request_id = p_request_id;

--    dbms_output.put_line('Previous request_id=' || previous_request_var);
    IF (previous_request_var < 1) THEN
      RETURN;
    END IF;

    l_message := 'Looking up request state for previous request ID ' || previous_request_var;
--    dbms_output.put_line('Looking up request state for previous request ID ' || previous_request_var);
    SELECT rs.request_state_id, rs.state_type_cd
      INTO state_id_var, state_type_var
      FROM request_state rs, request r
     WHERE r.request_id = rs.request_id
       AND rs.end_event_id IS NULL
       AND r.request_id = previous_request_var;

--    dbms_output.put_line('Found state_type_var ' || state_type_var);
    IF (state_type_var NOT IN ('C', 'E', 'HISTORICAL')) THEN
       event_id_var := p_event_id;
       IF (event_id_var < 1) THEN
          l_message := 'Getting event_id from sequence ';
          SELECT event_seq.NEXTVAL
            INTO event_id_var
            FROM dual;

          l_message := 'Inserting into event with event_id ' || event_id_var;
          INSERT INTO event (event_id, event_type_cd, event_timestamp)
            VALUES (event_id_var, 'SYST', sysdate);
       END IF;

--       dbms_output.put_line('Updating state_id ' || state_id_var);
       l_message := 'Updating request_state.end_event_id with event_id ' || event_id_var;
       dbms_output.put_line('Updating request_state.end_event_id with event_id ' || event_id_var);
       UPDATE request_state rs
          SET rs.end_event_id = event_id_var
        WHERE rs.request_state_id = state_id_var;

       l_message := 'Inserting into request_state with start_event_id ' || event_id_var;
--       dbms_output.put_line('Inserting into request_state with start_event_id ' || event_id_var);
       INSERT INTO request_state (request_state_id, request_id, state_type_cd, start_event_id)
            VALUES (request_state_seq.NEXTVAL, previous_request_var, 'C', event_id_var);

    END IF;

  EXCEPTION
    WHEN OTHERS THEN
      application_log_insert('nro_datapump_pkg', SYSDATE, 1, string_limit( 'Exception in ' ||
                             l_unit_name || '; ' || l_message || '; SQLERRM: ' || SQLERRM, 4000));
      ROLLBACK;
  END;


  PROCEDURE update_consent(p_request_id IN request.request_id%TYPE,
                           p_consent_flag IN VARCHAR2,
                           p_event_id IN event.event_id%TYPE) IS
    l_message APPLICATION_LOG.LOG_MESSAGE%TYPE;
    l_unit_name VARCHAR2(100);
    consent_count_var INTEGER := 0;
    consent_id_var consent.consent_id%TYPE := 0;
    received_var consent.received_flag%TYPE;
  BEGIN
    l_unit_name := 'update_consent';

    IF (p_consent_flag IS NULL OR LENGTH(p_consent_flag) = 0) THEN
      RETURN;
    END IF;

    IF (p_request_id < 1 OR p_event_id < 1) THEN
      RETURN;
    END IF;

   l_message := 'Checking if name consent already exists for request ' || p_request_id;
   dbms_output.put_line(l_message);
   SELECT COUNT(*), MAX(c.consent_id)
     INTO consent_count_var, consent_id_var
     FROM consent c
    WHERE c.request_id = p_request_id
      AND c.consent_type_cd = 'NAME';

   IF (consent_count_var > 1) THEN
      l_message := 'Updating end event id for ' || consent_count_var || ' records.';
      dbms_output.put_line(l_message);
     UPDATE consent c
        SET c.end_event_id = p_event_id
      WHERE c.consent_type_cd = 'NAME'
        AND c.request_id = p_request_id
        AND c.consent_id != consent_id_var;
   END IF;

   IF (consent_count_var > 0) THEN
      l_message := 'Checking consent_flag for consent id ' || consent_id_var;
      dbms_output.put_line(l_message);
      SELECT c.received_flag
       INTO received_var
       FROM consent c
      WHERE c.consent_id = consent_id_var;

      dbms_output.put_line('Existing received=' || received_var);
      IF (received_var = p_consent_flag) THEN
        RETURN;
      END IF;
   END IF;

  l_message := 'Inserting into consent with start_event_id=' || p_event_id || ',consent flag=' || p_consent_flag;
  dbms_output.put_line(l_message);
  INSERT INTO consent (consent_id, request_id, consent_type_cd,
                       start_event_id, received_flag)
       VALUES (consent_seq.NEXTVAL, p_request_id, 'NAME', p_event_id, p_consent_flag);

  EXCEPTION
    WHEN OTHERS THEN
      application_log_insert('nro_datapump_pkg', SYSDATE, 1, string_limit( 'Exception in ' ||
                             l_unit_name || '; ' || l_message || '; SQLERRM: ' || SQLERRM, 4000));
      ROLLBACK;
  END;


/*
**
** PROCEDURE update_request_state
**
** PURPOSE: update the request_state from datapump after a name request
**          has been processed.
**
** COMMENTS:
** Updates to a state of COMPLETED.
** Conditionally creates a consent record if consent_flag is 'Y'.
** Conditionally updates request_instance expiration date if expiry_date
** is not null.
**
**
*/
  PROCEDURE update_request_state(nr_number IN VARCHAR2,
                                 status IN VARCHAR2,
                                 expiry_date IN VARCHAR2,
                                 consent_flag IN VARCHAR2,
                                 examiner_id IN VARCHAR2,
                                 exam_comment IN VARCHAR2 DEFAULT NULL,
                                 add_info IN VARCHAR2 DEFAULT NULL,
                                 p_corp_num IN VARCHAR2 DEFAULT NULL) IS
    l_message APPLICATION_LOG.LOG_MESSAGE%TYPE;
    l_unit_name VARCHAR2(100);
    request_id_var NUMBER := 0;
    event_id_var NUMBER := 0;
    consent_count_var INTEGER := 0;
    current_state_type_var request_state.state_type_cd%TYPE;
    expiry_date_var request_instance.expiration_date%TYPE;
    request_type_var request_instance.request_type_cd%TYPE;
    name_instance_id_var name_instance.name_instance_id%TYPE;
    name_state_id_var name_state.name_state_id%TYPE;
    ri_rec request_instance%ROWTYPE;

  BEGIN
    l_unit_name := 'update_request_state';
    IF (status NOT IN ('A', 'R', 'H')) THEN
      RETURN;
    END IF;

    l_message := 'Updating system_variable code DP_REQUEST_TS to current timestamp';
    UPDATE system_variable s
       SET s.value = TO_CHAR(sysdate, 'YYYY-MM-DD HH24:MI:SS')
     WHERE s.code = 'DP_REQUEST_TS';
    COMMIT;

    l_message := 'Getting request_id for NR number ' || nr_number;
    dbms_output.put_line(l_message);
    SELECT r.REQUEST_ID
      INTO request_id_var
      FROM request r
     WHERE r.NR_NUM = nr_number;

    l_message := 'Getting active status for request id ' || request_id_var;
    dbms_output.put_line(l_message);
    SELECT rs.state_type_cd
      INTO current_state_type_var
      FROM request_state rs
     WHERE rs.request_id = request_id_var
       AND rs.end_event_id IS NULL;

    -- Do nothing if still in held state
    IF (status = 'H' AND current_state_type_var = 'H') THEN
      RETURN;
    -- Only change status - and only if current status is Draft
    ELSIF (status = 'H' AND current_state_type_var = 'D') THEN
       event_id_var := get_event;
       update_state(request_id_var, event_id_var, 'H', examiner_id, exam_comment);

    ELSIF (status = 'H' AND current_state_type_var = 'COMPLETED') THEN
       event_id_var := get_event;
       dbms_output.put_line('Resetting request: state returned to H from COMPLETED');
       update_state(request_id_var, event_id_var, 'H', examiner_id, exam_comment);

       l_message := 'RESET closing out consent records for request_id ' || request_id_var;
       dbms_output.put_line(l_message);
       UPDATE consent c
          SET c.end_event_id = event_id_var
        WHERE c.request_id = request_id_var;

       l_message := 'RESET deleting name_rule records for request_id ' || request_id_var;
       dbms_output.put_line(l_message);
       DELETE
         FROM name_rule nr
        WHERE nr.name_id IN (SELECT n.name_id FROM name n WHERE n.request_id = request_id_var);

       l_message := 'RESET updating name_state records for request_id ' || request_id_var;
       dbms_output.put_line(l_message);
       UPDATE name_state ns
          SET ns.name_state_type_cd = 'NE',
              ns.state_comment = null
        WHERE ns.name_id IN (SELECT n.name_id FROM name n WHERE n.request_id = request_id_var)
          AND ns.end_event_id IS NULL;

       l_message := 'RESET updating request_instance for request_id ' || request_id_var;
       dbms_output.put_line(l_message);
       UPDATE request_instance ri
          SET ri.expiration_date = NULL
        WHERE ri.request_id = request_id_var
          AND ri.end_event_id IS NULL;

    ELSE
       IF (status = 'A') THEN
/*
        BEGIN
          l_message := 'Request approved: deleting name_rule records for request_id ' || request_id_var;
          dbms_output.put_line(l_message);
          DELETE
            FROM name_rule nr
           WHERE nr.name_id IN (SELECT n.name_id FROM name n WHERE n.request_id = request_id_var);
        EXCEPTION
          WHEN OTHERS THEN
            l_message := '';
        END;
*/
        IF (consent_flag IN ('', 'N')) THEN
           BEGIN
             event_id_var := get_event;
             l_message := 'Request approved: closing consent records for request_id ' || request_id_var;
             dbms_output.put_line(l_message);
             UPDATE consent c
                SET c.end_event_id = event_id_var
              WHERE c.request_id = request_id_var;
           EXCEPTION
             WHEN OTHERS THEN
               l_message := '';
           END;
        END IF;

       END IF;

       IF (expiry_date IS NOT NULL AND LENGTH(expiry_date) = 8 AND status = 'A') THEN
         l_message := 'Looking up existing expiry date for request_id ' || request_id_var;
         dbms_output.put_line(l_message);
         SELECT ri.*
           INTO ri_rec
           FROM request_instance ri
          WHERE ri.request_id = request_id_var
            AND ri.end_event_id IS NULL;

         -- only update if expiry date has not been set
         IF (ri_rec.expiration_date IS NULL) THEN
           request_type_var := ri_rec.request_type_cd;
           IF (request_type_var IN ('AS', 'AL', 'UA')) THEN
             request_type_var := get_assumed_request_type(request_id_var);
             IF (request_type_var = '') THEN
               request_type_var := ri_rec.request_type_cd;
             END IF;
           END IF;
           IF (INSTR(RESTORATION_TYPES, ' ' || request_type_var || ' ') > 0) THEN
             expiry_date_var := TO_DATE(expiry_date, 'YYYYMMDD') + 365;
           ELSE
             expiry_date_var := TO_DATE(expiry_date, 'YYYYMMDD');
           END IF;

           IF (event_id_var = 0) THEN
             event_id_var := get_event;
           END IF;
           l_message := 'Updating request_instance for request_id ' || request_id_var;
           dbms_output.put_line(l_message);
           UPDATE request_instance ri
              SET ri.end_event_id = event_id_var
            WHERE ri.request_id = request_id_var
              AND ri.end_event_id IS NULL;

           l_message := 'Inserting into request_instance for request_id ' || request_id_var;
           dbms_output.put_line(l_message);
          INSERT INTO request_instance(request_instance_id,
                                       request_id,
                                       priority_cd,
                                       request_type_cd,
                                       expiration_date,
                                       start_event_id,
                                       end_event_id,
                                       xpro_jurisdiction,
                                       queue_position,
                                       additional_info,
                                       tilma_ind,
                                       nuans_expiration_date,
                                       nuans_num,
                                       assumed_nuans_num,
                                       assumed_nuans_name,
                                       assumed_nuans_expiration_date,
                                       last_nuans_update_role,
                                       tilma_transaction_id)
              VALUES(request_instance_seq.nextval,
                     request_id_var,
                     ri_rec.priority_cd,
                     ri_rec.request_type_cd,
                     expiry_date_var,
                     event_id_var,
                     null,
                     ri_rec.xpro_jurisdiction,
                     ri_rec.queue_position,
                     add_info,
                     ri_rec.tilma_ind,
                     ri_rec.nuans_expiration_date,
                     ri_rec.nuans_num,
                     ri_rec.assumed_nuans_num,
                     ri_rec.assumed_nuans_name,
                     ri_rec.assumed_nuans_expiration_date,
                     ri_rec.last_nuans_update_role,
                     ri_rec.tilma_transaction_id);
         END IF;
       END IF;

       IF (current_state_type_var != 'COMPLETED') THEN
        IF (event_id_var = 0) THEN
          event_id_var := get_event;
        END IF;

        l_message := 'Updating request_state.end_event_id with event_id ' || event_id_var;
        dbms_output.put_line(l_message);
          UPDATE request_state rs
             SET rs.end_event_id = event_id_var
           WHERE rs.request_id = request_id_var
             AND rs.end_event_id IS NULL;

          l_message := 'Inserting into request_state with start_event_id ' || event_id_var;
          dbms_output.put_line(l_message);
          INSERT INTO request_state (request_state_id, request_id, state_type_cd,
                                     start_event_id, examiner_idir, examiner_comment)
               VALUES (request_state_seq.NEXTVAL, request_id_var, 'COMPLETED', event_id_var, examiner_id, exam_comment);
       END IF;

       IF (consent_flag IN ('Y', 'R')) THEN
         l_message := 'Checking if name consent already exists ';
         dbms_output.put_line(l_message);
         SELECT COUNT(*)
           INTO consent_count_var
           FROM consent c
          WHERE c.request_id = request_id_var
            AND c.end_event_id IS NULL
            AND c.consent_type_cd = 'NAME'
            AND c.received_flag IN ('Y', 'R');
         -- Only update once: maintained by NRO after examined.
         IF (consent_count_var = 0) THEN
           IF (event_id_var = 0) THEN
             event_id_var := get_event;
           END IF;

           l_message := 'Inserting into consent with start_event_id ' || event_id_var;
           dbms_output.put_line(l_message);
           INSERT INTO consent (consent_id, request_id, consent_type_cd,
                                start_event_id, received_flag)
                VALUES (consent_seq.NEXTVAL, request_id_var, 'NAME', event_id_var, consent_flag);

            -- Transition name state to 'C' if currently 'A'.
           l_message := 'Looking up Approved name for request ' || request_id_var;
           dbms_output.put_line(l_message);
           BEGIN
              SELECT NVL(ns.name_state_id, 0)
                INTO name_state_id_var
                FROM request r, name n, name_state ns
               WHERE r.request_id = n.request_id
                 AND r.request_id = request_id_var
                 AND n.name_id = ns.name_id
                 AND ns.end_event_id IS NULL
                 AND ns.name_state_type_cd = 'A';
               IF (name_state_id_var > 0) THEN
                 l_message := 'Updating name_state from A to C for state id ' || name_state_id_var;
                 UPDATE name_state ns
                    SET ns.name_state_type_cd = 'C'
                  WHERE ns.name_state_id = name_state_id_var;
               END IF;
            EXCEPTION
              WHEN OTHERS THEN
                name_state_id_var := 0;
            END;
         END IF;

       END IF;

       IF (status = 'A' AND p_corp_num IS NOT NULL AND LENGTH(TRIM(p_corp_num)) > 0) THEN
         l_message := 'Checking if name already consumed for corp_num ' || p_corp_num;
         dbms_output.put_line(l_message);
         SELECT MAX(ni.name_instance_id)
           INTO name_instance_id_var
           FROM name n, name_state ns, name_instance ni
          WHERE n.request_id = request_id_var
            AND n.name_id = ns.name_id
            AND ns.name_state_type_cd IN ('A', 'C')
            AND ni.name_id = n.name_id
            AND ni.corp_num IS NULL
            AND ns.end_event_id IS NULL;

         IF (name_instance_id_var IS NOT NULL AND name_instance_id_var > 0) THEN
           l_message := 'Updating corp_num for name_instance_id ' || name_instance_id_var;
           dbms_output.put_line(l_message);
           UPDATE name_instance ni
              SET ni.corp_num = p_corp_num
            WHERE ni.name_instance_id = name_instance_id_var;
         END IF;
       END IF;

       IF (status IN ('A', 'R')) THEN
         cancel_resubmit(request_id_var, event_id_var);
       END IF;
    END IF;

    COMMIT;

  EXCEPTION
    WHEN OTHERS THEN
      application_log_insert('nro_datapump_pkg', SYSDATE, 1, string_limit( 'Exception in ' ||
                             l_unit_name || '; ' || l_message || '; SQLERRM: ' || SQLERRM, 4000));
      ROLLBACK;
  END;


/*
**
** PROCEDURE update_name_state
**
** PURPOSE: update the name_state from datapump after a name request
**          has been processed.
**
** COMMENTS:
** Updates to a state of A or R.
**
**
*/
  PROCEDURE update_name_state(nr_number IN VARCHAR2,
                              name_choice IN VARCHAR2,
                              accept_reject_flag IN VARCHAR2,
                              reject_condition IN VARCHAR2 DEFAULT NULL) IS
    l_message APPLICATION_LOG.LOG_MESSAGE%TYPE;
    l_unit_name VARCHAR2(100);
    name_state_id_var NAME_STATE.NAME_STATE_ID%TYPE;
    name_id_var NAME_STATE.NAME_ID%TYPE;
    event_id_var NAME_STATE.START_EVENT_ID%TYPE;
    request_state_var VARCHAR2(20);
    consent_count_var NUMBER := 0;
    request_id_var request.request_id%TYPE;
    state_type_var name_state.name_state_type_cd%TYPE;
    current_state_var name_state.name_state_type_cd%TYPE;
  BEGIN
    l_unit_name := 'update_name_state';

    l_message := 'Updating system_variable code DP_REQNAME_TS to current timestamp';
    UPDATE system_variable s
       SET s.value = TO_CHAR(sysdate, 'YYYY-MM-DD HH24:MI:SS')
     WHERE s.code = 'DP_REQNAME_TS';
    COMMIT;

    IF (accept_reject_flag IS NULL OR TRIM(accept_reject_flag) = '' OR
        accept_reject_flag NOT IN ('A', 'R')) THEN
      RETURN;
    END IF;

    l_message := 'Looking up request state, request id for ' || nr_number;
    dbms_output.put_line(l_message);
    SELECT rs.state_type_cd, r.request_id
      INTO request_state_var, request_id_var
      FROM request r, request_state rs
     WHERE r.request_id = rs.request_id
       AND r.nr_num = nr_number
       AND rs.end_event_id IS NULL;
    IF (request_state_var NOT IN ('D', 'COMPLETED', 'H')) THEN
      dbms_output.put_line('request state ' || request_state_var || ' : aborting');
      RETURN;
    END IF;

    l_message := 'Getting name_state_id for NR number ' || nr_number || ', choice= ' || name_choice;
    dbms_output.put_line(l_message);
    SELECT ns.name_state_id, ns.name_state_type_cd
      INTO name_state_id_var, current_state_var
      FROM request r, name n, name_instance ni, name_state ns
     WHERE r.NR_NUM = nr_number
       AND r.request_id = n.request_id
       AND n.name_id = ni.name_id
       AND ni.end_event_id IS NULL
       AND TO_CHAR(ni.choice_number) = name_choice
       AND n.name_id = ns.name_id
       AND ns.end_event_id IS NULL;

    state_type_var := accept_reject_flag;
    IF (state_type_var = 'A') THEN
       l_message := 'Checking if consent required for request id ' || request_id_var;
      dbms_output.put_line(l_message);
      SELECT COUNT(*)
        INTO consent_count_var
        FROM consent c
       WHERE c.request_id = request_id_var
         AND c.end_event_id IS NULL
         AND c.consent_type_cd = 'NAME'
         AND c.received_flag IN ('Y', 'R');
      IF (consent_count_var > 0) THEN
       state_type_var := 'C';
       dbms_output.put_line('Updating name state from A to C: consent count=' || consent_count_var);
      END IF;
    END IF;

    IF (current_state_var = state_type_var) THEN
       dbms_output.put_line('Current state identical to new state');
      RETURN;
    END IF;

    l_message := 'Getting name_id for name_state_id ' || name_state_id_var || ' current state=' || current_state_var;
    dbms_output.put_line(l_message);
    SELECT ns.name_id
      INTO name_id_var
      FROM name_state ns
     WHERE ns.name_state_id = name_state_id_var;

    event_id_var := get_event;

    l_message := 'Updating name_state.end_event_id with name_id ' || name_id_var || ' request_id ' || request_id_var || ' event_id=' || event_id_var;
    dbms_output.put_line(l_message);
    UPDATE name_state ns
       SET ns.end_event_id = event_id_var
     WHERE ns.name_id = name_id_var
       AND ns.end_event_id IS NULL;

    l_message := 'Inserting into name_state type= ' || state_type_var || ' for start_event_id ' || event_id_var;
    dbms_output.put_line(l_message);
    INSERT INTO name_state (name_state_id, name_id, start_event_id, name_state_type_cd, state_comment)
         VALUES (name_state_seq.NEXTVAL, name_id_var, event_id_var, state_type_var, reject_condition);

    COMMIT;

  EXCEPTION
    WHEN OTHERS THEN
      application_log_insert('nro_datapump_pkg', SYSDATE, 1, string_limit( 'Exception in ' ||
                             l_unit_name || '; ' || l_message || '; SQLERRM: ' || SQLERRM, 4000));
  END;


/*
**
** PROCEDURE update_name_rule
**
** PURPOSE: Insert into the name_rule table data from the datapump to capture
**          conflicting name, conflicting company number information.
**
** COMMENTS:
** Reason code is CONFLICT.
**
**
*/
  PROCEDURE update_name_rule(nr_number IN VARCHAR2,
                             name_choice IN VARCHAR2,
                             conflicting_number IN VARCHAR2,
                             conflicting_name IN VARCHAR2) IS
    l_message APPLICATION_LOG.LOG_MESSAGE%TYPE;
    l_unit_name VARCHAR2(100);
    name_id_var NUMBER := 0;
    request_state_var VARCHAR2(20);
    conf_count_var INTEGER := 0;

    BEGIN
    l_unit_name := 'update_name_rule';

    IF (conflicting_name IS NULL AND conflicting_number IS NULL) THEN
      RETURN;
    END IF;

    l_message := 'Updating system_variable code DP_CONFLICT_TS to current timestamp';
    dbms_output.put_line(l_message);
    UPDATE system_variable s
       SET s.value = TO_CHAR(sysdate, 'YYYY-MM-DD HH24:MI:SS')
     WHERE s.code = 'DP_CONFLICT_TS';
    COMMIT;

    l_message := 'Checking request state for ' || nr_number;
    dbms_output.put_line(l_message);
    SELECT rs.state_type_cd
      INTO request_state_var
      FROM request r, request_state rs
     WHERE r.request_id = rs.request_id
       AND r.nr_num = nr_number
       AND rs.end_event_id IS NULL;
    IF (request_state_var NOT IN ('D', 'H', 'COMPLETED')) THEN
      dbms_output.put_line('request state ' || request_state_var || ' : aborting');
      RETURN;
    END IF;

    l_message := 'Getting name_id for NR number ' || nr_number || ' choice=' || name_choice;
    dbms_output.put_line(l_message);
    SELECT n.name_id
      INTO name_id_var
      FROM request r, name n, name_instance ni
     WHERE r.NR_NUM = nr_number
       AND r.request_id = n.request_id
       AND n.name_id = ni.name_id
       AND ni.end_event_id IS NULL
       AND TO_CHAR(ni.choice_number) = name_choice;

    IF (conflicting_name IS NOT NULL) THEN
--      DBMS_LOCK.sleep(0.02);
       l_message := 'Checking existing conflicts for ' || name_id_var || ': ' || conflicting_name;
       dbms_output.put_line(l_message);
       SELECT COUNT(nr.name_id)
         INTO conf_count_var
         FROM name_rule nr
        WHERE nr.name_id = name_id_var
          AND nr.conf_name IS NOT NULL
          AND nr.conf_name = conflicting_name;
       IF (conf_count_var > 0) THEN
         dbms_output.put_line(conf_count_var || ' records for ' || name_id_var || ' already exist with conf_name=' || conflicting_name);
         RETURN;
       END IF;
    END IF;

    l_message := 'Inserting into name_rule for name_id ' || name_id_var;
    dbms_output.put_line(l_message);
    INSERT INTO name_rule (name_id, name_rule_id, reject_reason_cd,
                           rule_id, conf_number, conf_name, rejected_by)
         VALUES (name_id_var, name_rule_seq.NEXTVAL, 'CONFLICT', 1, conflicting_number, conflicting_name, 'EXAMINER');

    COMMIT;

  EXCEPTION
    WHEN OTHERS THEN
      application_log_insert('nro_datapump_pkg', SYSDATE, 1, string_limit( 'Exception in ' ||
                             l_unit_name || '; ' || l_message || '; SQLERRM: ' || SQLERRM, 4000));
  END;


  --
  -- Make non-colin entity historical if a name is found that
  -- matches the corp_type corp_num pair and the request is
  -- currently in a completed state.
  --
  PROCEDURE make_historical(p_corp_num IN VARCHAR2,
                            p_corp_type IN VARCHAR2,
                            p_corp_name IN VARCHAR2 DEFAULT NULL) IS
    l_message APPLICATION_LOG.LOG_MESSAGE%TYPE;
    l_unit_name VARCHAR2(100);
    request_state_var VARCHAR2(20);
    request_id_var request.request_id%TYPE;
    corp_num_var VARCHAR2(20);
    event_id_var NAME_STATE.START_EVENT_ID%TYPE;

  BEGIN
    l_unit_name := 'make_historical';

    l_message := 'Updating system_variable code DP_HISTORICAL_TS to current timestamp';
    UPDATE system_variable s
       SET s.value = TO_CHAR(sysdate, 'YYYY-MM-DD HH24:MI:SS')
     WHERE s.code = 'DP_HISTORY_TS';
    COMMIT;

    corp_num_var := p_corp_type || p_corp_num;
    l_message := 'Looking up request_id for corp_num ' || corp_num_var;
    BEGIN
       SELECT MAX(n.request_id)
         INTO request_id_var
         FROM name n, name_instance ni
        WHERE n.name_id = ni.name_id
          AND ni.corp_num = corp_num_var;
    EXCEPTION
      WHEN OTHERS THEN
        RETURN;
    END;

    IF (request_id_var IS NULL OR TRIM(request_id_var) = '') THEN
--      application_log_insert('nro_datapump_pkg', SYSDATE, 1, string_limit(l_unit_name || '; ' || l_message || '; TESTING', 4000));
      RETURN;
    END IF;

    l_message := 'Looking up request_state for request_id ' || request_id_var;
    SELECT rs.state_type_cd
      INTO request_state_var
      FROM request_state rs
     WHERE rs.request_id = request_id_var
       AND rs.end_event_id IS NULL;
    IF (request_state_var = 'HISTORICAL') THEN
--      dbms_output.put_line('request state ' || request_state_var || ' : aborting');
--      application_log_insert('nro_datapump_pkg', SYSDATE, 1, string_limit(l_unit_name || '; ' || l_message || '; TESTING'));
      RETURN;
    END IF;

    l_message := 'Getting event_id from sequence ';
    SELECT event_seq.NEXTVAL
      INTO event_id_var
      FROM dual;

    l_message := 'Inserting into event with event_id ' || event_id_var;
    INSERT INTO event (event_id, event_type_cd, event_timestamp)
      VALUES (event_id_var, 'SYST', sysdate);

    l_message := 'Updating request_state.end_event_id with event_id ' || event_id_var;
    UPDATE request_state rs
       SET rs.end_event_id = event_id_var
     WHERE rs.request_id = request_id_var
       AND rs.end_event_id IS NULL;

    l_message := 'Inserting into request_state with start_event_id ' || event_id_var;
    INSERT INTO request_state (request_state_id, request_id, state_type_cd, start_event_id)
         VALUES (request_state_seq.NEXTVAL, request_id_var, 'HISTORICAL', event_id_var);
    COMMIT;

  EXCEPTION
    WHEN OTHERS THEN
      application_log_insert('nro_datapump_pkg', SYSDATE, 1, string_limit( 'Exception in ' ||
                             l_unit_name || '; ' || l_message || '; SQLERRM: ' || SQLERRM, 4000));
  END;


  --
  -- Consume requests for non-colin request types. Find
  -- approved name matching the supplied NR and update the
  -- corp number.
  --
  PROCEDURE consume_request(p_nr_num IN VARCHAR2,
                            p_corp_num IN VARCHAR2) IS
    l_unit_name   VARCHAR2(100);
    l_message   VARCHAR2(256);
    l_corp_num name_instance.corp_num%TYPE;
    l_count INTEGER;
  BEGIN
    l_unit_name := 'consume_request ';

    IF (p_nr_num = null OR TRIM(p_nr_num) = '') THEN
      RETURN;
    END IF;
    IF (p_corp_num = null OR TRIM(p_corp_num) = '') THEN
      RETURN;
    END IF;

    l_message := l_unit_name || 'Updating system_variable code DP_CONSUME_TS to current timestamp';
    log_debug(l_message);
    UPDATE system_variable s
       SET s.value = TO_CHAR(sysdate, 'YYYY-MM-DD HH24:MI:SS')
     WHERE s.code = 'DP_CONSUME_TS';
    COMMIT;

    l_count := 0;
    l_message := l_unit_name || 'Checking if ' || p_nr_num || ' already consumed.';
    log_debug(l_message);
    -- Check if already consumed: this should be a one-time event
    -- so do not overwrite the existing consuming corp number.
      SELECT COUNT(ni.name_instance_id)
        INTO l_count
        FROM  name_instance ni, name n, request r, name_state ns
       WHERE r.request_id = n.request_id
         AND n.name_id = ni.name_id
         AND ni.name_id = ns.name_id
         AND ns.name_state_type_cd IN ('A', 'C')
         AND ns.end_event_id IS NULL
         AND ni.end_event_id IS NULL
         AND r.nr_num = TRIM(p_nr_num)
         AND ni.corp_num IS NULL;

    IF (l_count < 1) THEN
      l_message := l_unit_name || p_nr_num || ' already consumed - not consuming with corpNum=' || p_corp_num;
      log_debug(l_message);
      application_log_insert('nro_datapump_pkg', SYSDATE, 2, l_message);
      RETURN;
    END IF;

    l_corp_num := format_corp_num(p_corp_num);
    l_message := l_unit_name || 'Updating name_instance.corp_num to ' || l_corp_num || ' for nr ' || p_nr_num;
    log_debug(l_message);
      UPDATE name_instance ni2
         SET ni2.corp_num = l_corp_num
       WHERE ni2.name_instance_id IN (SELECT  ni.name_instance_id
                                         FROM  name_instance ni, name n, request r, name_state ns
                                        WHERE r.request_id = n.request_id
                                          AND n.name_id = ni.name_id
                                          AND ni.name_id = ns.name_id
                                          AND ns.name_state_type_cd IN ('A', 'C')
                                          AND ns.end_event_id IS NULL
                                          AND ni.end_event_id IS NULL
                                          AND r.nr_num = TRIM(p_nr_num))
        AND ni2.end_event_id IS NULL;
    COMMIT;

  EXCEPTION
    WHEN OTHERS THEN
      log_debug(l_unit_name || 'failed: ' || SQLERRM);
      application_log_insert('nro_datapump_pkg', SYSDATE, 1, string_limit( 'Exception in ' ||
                             l_message || '; SQLERRM: ' || SQLERRM, 4000));
  END;



/*
**
** FUNCTION dummy
**
** Purpose: used to validate the state of the package
**
*/
  FUNCTION dummy RETURN VARCHAR2 IS
    l_dummy VARCHAR2(1);

  BEGIN
    l_dummy := 'X';

    RETURN l_dummy;
  END;
    
/*
**l_corp_num := format_corp_num(p_corp_num);l_corp_num := format_corp_num(p_corp_num);
** FUNCTION name_examination_func
**
** PURPOSE: Giving caller a return message if name_examination_func is failed. Otherwise, it will return empty string. 
**
** COMMENTS:
**
*/
FUNCTION name_examination_func(p_nr_number IN VARCHAR2,
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
                                  p_confname3C IN VARCHAR2 DEFAULT 'NA'
                                  ) RETURN VARCHAR2 IS

    l_unit_name   VARCHAR2(100);
    l_message   VARCHAR2(4000);
    l_return   VARCHAR2(32500);

    l_request_id NUMBER := 0;
    l_event_id NUMBER := 0;
    l_current_state_type request_state.state_type_cd%TYPE;
    l_expiry_date request_instance.expiration_date%TYPE;
    l_request_type request_instance.request_type_cd%TYPE;
    l_name_state_id name_state.name_state_id%TYPE;
    ri_rec request_instance%ROWTYPE;
    ns_rec name_state%ROWTYPE;
    ni_rec name_instance%ROWTYPE;
    l_state_code name_state.name_state_type_cd%TYPE;
    l_state_comment varchar2(1000);
    l_conf_number name_rule.conf_number%TYPE;
    l_conf_name name_rule.conf_name%TYPE;

    
    CURSOR name_state_cur(p_request_id name.request_id%TYPE) IS
       SELECT *
         FROM name_state ns
        WHERE ns.name_id IN (SELECT n.name_id FROM name n WHERE n.request_id = p_request_id)
          AND ns.end_event_id IS NULL;

    CURSOR name_instance_cur(p_request_id name.request_id%TYPE) IS
       SELECT *
         FROM name_instance ni
        WHERE ni.name_id IN (SELECT n.name_id FROM name n WHERE n.request_id = p_request_id)
          AND ni.end_event_id IS NULL;        
              
  
    BEGIN 
        l_unit_name := 'name_examination_func';
        l_return := '';
        
        IF (p_status NOT IN ('A', 'R', 'H')) THEN
          RETURN l_return;
        END IF;        
            
        l_message := l_unit_name || ' updating system_variable code DP_REQUEST_TS to current timestamp';
        UPDATE system_variable s
           SET s.value = TO_CHAR(sysdate, 'YYYY-MM-DD HH24:MI:SS')
         WHERE s.code = 'DP_REQUEST_TS';
        COMMIT;                 
                   
            
        l_message := l_unit_name || ' getting request_id, state code for NR number ' || p_nr_number;
        log_debug(l_message);
        SELECT r.REQUEST_ID, rs.state_type_cd
          INTO l_request_id, l_current_state_type
          FROM request r, request_state rs
         WHERE r.NR_NUM = p_nr_number
           AND r.request_id = rs.request_id
           AND rs.end_event_id IS NULL;   
            
            
         log_debug(l_unit_name || ' requestId= ' || l_request_id || ' existing stateCode=' || 
                   l_current_state_type || ' incoming stateCode=' || p_status); 
             
            -- Do nothing if states have not changed (still in held state)
         IF (p_status = 'H' AND l_current_state_type = 'H' OR
            (l_current_state_type = 'COMPLETED' AND p_status IN ('A', 'R'))) THEN
           RETURN l_return;
         END IF;       
             
        -- Only change status - and only if current status is Draft            
      IF (p_status = 'H' AND l_current_state_type = 'D') THEN
           log_debug(l_unit_name || ' HELD state update only');
           l_event_id := get_event;
           l_message := l_unit_name || ' updating request_state for requestId=' || l_request_id || ' eventId=' || l_event_id;
           update_state(l_request_id, l_event_id, 'H', TRIM(p_examiner_id), p_exam_comment);
           log_debug(l_unit_name || ' HELD state update committing changes');
           COMMIT;
           RETURN l_return;
        END IF;
         
         -- If get to here either reset or name examination 
        l_message := l_unit_name || ' getting event_id for event_type ' || 'EXAM';
        l_event_id := get_event('EXAM');
        
        
        -- Resetting request                  
        IF (p_status = 'H' AND l_current_state_type = 'COMPLETED') THEN
           log_debug(l_unit_name || ' RESET resetting request: state returned to H from COMPLETED');
    
           l_message := l_unit_name || ' RESET inserting transaction for requestId=' || l_request_id || ' eventId=' || l_event_id;
           log_debug(l_message);
           INSERT INTO transaction(transaction_id, transaction_type_cd, request_id, event_id, bcol_racf_id)
                  VALUES(transaction_seq.nextval, 'RESET', l_request_id, l_event_id, TRIM(p_examiner_id));    
           
           update_state(l_request_id, l_event_id, 'H', TRIM(p_examiner_id), p_exam_comment);
    
           l_message := l_unit_name || ' RESET closing out consent records for request_id ' || l_request_id;
           log_debug(l_message);
           UPDATE consent c
              SET c.end_event_id = l_event_id
            WHERE c.request_id = l_request_id;   
        
           l_message := l_unit_name || ' RESET deleting name_rule records for request_id ' || l_request_id;
           dbms_output.put_line(l_message);
           DELETE
             FROM name_rule nr
            WHERE nr.name_id IN (SELECT n.name_id FROM name n WHERE n.request_id = l_request_id);
    
           l_message := l_unit_name || ' RESET updating name_state records for request_id ' || l_request_id;
           log_debug(l_message);
            FOR ns_rec in name_state_cur(l_request_id) LOOP
              UPDATE name_state ns
                 SET ns.end_event_id = l_event_id
                WHERE ns.name_state_id = ns_rec.name_state_id;
              INSERT INTO name_state(name_state_id,name_id,start_event_id,end_event_id,name_state_type_cd,state_comment)
                    VALUES(name_state_seq.nextval, ns_rec.name_id, l_event_id, NULL, 'NE', null);
            END LOOP;
    
           l_message := l_unit_name || ' RESET getting record in request_instance for request_id ' || l_request_id;
           log_debug(l_message);
            SELECT ri.*
              INTO ri_rec
              FROM request_instance ri
             WHERE ri.request_id = l_request_id
               AND ri.end_event_id IS NULL;
    
           l_message := l_unit_name || ' RESET updating request_instance for request_id ' || l_request_id;
           UPDATE request_instance ri
              SET ri.end_event_id = l_event_id
            WHERE ri.request_id = l_request_id
              AND ri.end_event_id IS NULL;
    
           l_message := l_unit_name || ' RESET inserting initial request_instance from request_instance_id ' || ri_rec.request_instance_id;
           log_debug(l_message);
           INSERT INTO request_instance(request_instance_id,
                                       request_id,
                                       priority_cd,
                                       request_type_cd,
                                       expiration_date,
                                       start_event_id,
                                       end_event_id,
                                       xpro_jurisdiction,
                                       queue_position,
                                       additional_info,
                                       tilma_ind,
                                       nuans_expiration_date,
                                       nuans_num,
                                       assumed_nuans_num,
                                       assumed_nuans_name,
                                       assumed_nuans_expiration_date,
                                       last_nuans_update_role,
                                       tilma_transaction_id, nature_business_info)
              VALUES(request_instance_seq.nextval,
                     ri_rec.request_id,
                     ri_rec.priority_cd,
                     ri_rec.request_type_cd,
                     null,
                     l_event_id,
                     null,
                     ri_rec.xpro_jurisdiction,
                     ri_rec.queue_position,
                     ri_rec.additional_info,
                     ri_rec.tilma_ind,
                     ri_rec.nuans_expiration_date,
                     ri_rec.nuans_num,
                     ri_rec.assumed_nuans_num,
                     ri_rec.assumed_nuans_name,
                     ri_rec.assumed_nuans_expiration_date,
                     ri_rec.last_nuans_update_role,
                     ri_rec.tilma_transaction_id,
                     ri_rec.nature_business_info);
           log_debug(l_unit_name || ' RESET committing changes');
           COMMIT;
           RETURN l_return;
        END IF;
            
        
        -- Request accepted or rejected
        l_message := l_unit_name || ' inserting NAME_EXAM transaction for requestId=' || l_request_id || ' eventId=' || l_event_id;
        log_debug(l_message);
        INSERT INTO transaction(transaction_id, transaction_type_cd, request_id, event_id, bcol_racf_id)
               VALUES(transaction_seq.nextval, 'NAME_EXAM', l_request_id, l_event_id, TRIM(p_examiner_id));
               
        IF (p_expiry_date IS NOT NULL AND LENGTH(p_expiry_date) = 8 AND p_status = 'A') THEN    
          l_message := l_unit_name || ' APPROVED NAME EXAM looking up existing request_instance for request_id ' || l_request_id;
          log_debug(l_message);
          SELECT ri.*
            INTO ri_rec
            FROM request_instance ri
           WHERE ri.request_id = l_request_id
             AND ri.end_event_id IS NULL;
    
            l_request_type := ri_rec.request_type_cd;
            IF (l_request_type IN ('AS', 'AL', 'UA')) THEN
              l_request_type := get_assumed_request_type(l_request_id);
              IF (l_request_type = '') THEN
                l_request_type := ri_rec.request_type_cd;
              END IF;
            END IF;
            IF (INSTR(RESTORATION_TYPES, ' ' || l_request_type || ' ') > 0) THEN
              l_expiry_date := TO_DATE(p_expiry_date, 'YYYYMMDD') + 365;
            ELSE
              l_expiry_date := TO_DATE(p_expiry_date, 'YYYYMMDD');
            END IF;
          
          l_message := l_unit_name || ' APPROVED NAME EXAM expiry date=' || l_expiry_date || ' updating request_instance';
          log_debug(l_message);
          UPDATE request_instance ri
             SET ri.end_event_id = l_event_id
           WHERE ri.request_id = l_request_id
             AND ri.end_event_id IS NULL;
    
          l_message := l_unit_name || ' APPROVED NAME EXAM inserting request_instance eventId=' || l_event_id || ' requestId=' || l_request_id;
          log_debug(l_message);
          INSERT INTO request_instance(request_instance_id,
                                     request_id,
                                     priority_cd,
                                     request_type_cd,
                                     expiration_date,
                                     start_event_id,
                                     end_event_id,
                                     xpro_jurisdiction,
                                     queue_position,
                                     additional_info,
                                     tilma_ind,
                                     nuans_expiration_date,
                                     nuans_num,
                                     assumed_nuans_num,
                                     assumed_nuans_name,
                                     assumed_nuans_expiration_date,
                                     last_nuans_update_role,
                                     tilma_transaction_id, nature_business_info)
            VALUES(request_instance_seq.nextval,
                   l_request_id,
                   ri_rec.priority_cd,
                   ri_rec.request_type_cd,
                   l_expiry_date,
                   l_event_id,
                   null,
                   ri_rec.xpro_jurisdiction,
                   ri_rec.queue_position,
    --               TRIM(p_add_info),
                   ri_rec.additional_info,
                   ri_rec.tilma_ind,
                   ri_rec.nuans_expiration_date,
                   ri_rec.nuans_num,
                   ri_rec.assumed_nuans_num,
                   ri_rec.assumed_nuans_name,
                   ri_rec.assumed_nuans_expiration_date,
                   ri_rec.last_nuans_update_role,
                   ri_rec.tilma_transaction_id,
                   ri_rec.nature_business_info);
    
           -- If accepted, conditionally create consent required/received record.
           IF (p_consent_flag IN ('Y', 'R')) THEN
               l_message := l_unit_name || ' APPROVED EXAM inserting into consent with start_event_id ' || l_event_id;
               log_debug(l_message);
               INSERT INTO consent (consent_id, request_id, consent_type_cd,
                                    start_event_id, received_flag)
                    VALUES (consent_seq.NEXTVAL, l_request_id, 'NAME', l_event_id, p_consent_flag);
           END IF;
         END IF;
    
          l_message := l_unit_name || ' NAME EXAM updating request_state.end_event_id with event_id ' || l_event_id;
          log_debug(l_message);
          UPDATE request_state rs
             SET rs.end_event_id = l_event_id
           WHERE rs.request_id = l_request_id
             AND rs.end_event_id IS NULL;
    
          l_message := l_unit_name || ' NAME EXAM inserting into request_state with event_id ' || l_event_id;
          log_debug(l_message);
          INSERT INTO request_state (request_state_id, request_id, state_type_cd,
                                   start_event_id, examiner_idir, examiner_comment)
               VALUES (request_state_seq.NEXTVAL, l_request_id, 'COMPLETED', l_event_id, TRIM(p_examiner_id), p_exam_comment);
    
          -- Now update name_state, name_rule
           l_message := l_unit_name || ' NAME_EXAM updating name_state records for request_id ' || l_request_id 
                        || ' choice1 length=' ||  LENGTH(p_choice1) || ' choice2 length=' ||  LENGTH(p_choice2)|| ' choice3 length=' ||  LENGTH(p_choice3);
           log_debug(l_message);
            FOR ni_rec in name_instance_cur(l_request_id) LOOP
              l_state_comment := '';
              IF (ni_rec.choice_number = 1) THEN
                 l_state_code := SUBSTR(TRIM(p_choice1), 1, 1);
                 IF (l_state_code IN ('A', 'R') AND LENGTH(p_choice1) > 5) THEN
                   l_message := l_unit_name || ' NAME_EXAM extracting state comment for choice 1: length=' || LENGTH(p_choice1);
                   l_state_comment := SUBSTR(p_choice1, 6);
                 END IF;
              ELSIF (ni_rec.choice_number = 2) THEN
                 l_state_code := SUBSTR(TRIM(p_choice2), 1, 1);
                 IF (l_state_code IN ('A', 'R') AND LENGTH(p_choice2) > 5) THEN
                   l_message := l_unit_name || ' NAME_EXAM extracting state comment for choice 2: length=' || LENGTH(p_choice2);
                   l_state_comment := SUBSTR(p_choice2, 6);
                 END IF;
              ELSE
                 l_state_code := SUBSTR(TRIM(p_choice3), 1, 1);
                 IF (l_state_code IN ('A', 'R') AND LENGTH(p_choice3) > 5) THEN
                   l_message := l_unit_name || ' NAME_EXAM extracting state comment for choice 3: length=' || LENGTH(p_choice3);
                   l_state_comment := SUBSTR(p_choice3, 6);
                 END IF;
              END IF;
    
              -- If not examined do not update record.
              IF (l_state_code IN ('A', 'R')) THEN
                IF (l_state_code = 'A' AND p_consent_flag IN ('Y', 'R')) THEN
                  l_state_code := 'C';
                END IF;
                l_message := l_unit_name || ' NAME_EXAM updating name_state for choice=' || ni_rec.choice_number ||
                             ' name_id=' || ni_rec.name_id || ' stateCode=' || l_state_code;
                log_debug(l_message);    
                 UPDATE name_state ns
                    SET ns.end_event_id = l_event_id
                   WHERE ns.name_id = ni_rec.name_id
                     AND ns.end_event_id IS NULL;
       
    
                 l_message := l_unit_name || ' NAME_EXAM inserting name_state for name_id=' || ni_rec.name_id || ' stateCode=' || l_state_code || ' event_id= ' || l_event_id; 
                 INSERT INTO name_state(name_state_id, name_id,start_event_id,end_event_id,name_state_type_cd,state_comment)
                       VALUES(name_state_seq.nextval, ni_rec.name_id, l_event_id, NULL, l_state_code, l_state_comment);
    
                 -- now insert conflicting names:
                 IF (ni_rec.choice_number = 1) THEN
                    IF (p_confname1a != 'NA' AND p_confname1a IS NOT NULL) THEN
                      l_conf_number := SUBSTR(p_confname1a, 1, (INSTR(p_confname1a, '****') - 1));
                      l_conf_name := SUBSTR(p_confname1a, (INSTR(p_confname1a, '****') + 4));
                      l_message := l_unit_name || ' NAME EXAM inserting into name_rule for name_id ' || ni_rec.name_id ||
                                   ' confNumber=' || l_conf_number || ' confName=' || l_conf_name;
                      log_debug(l_message);
                      INSERT INTO name_rule (name_id, name_rule_id, reject_reason_cd, rule_id, conf_number, conf_name, rejected_by)
                         VALUES (ni_rec.name_id, name_rule_seq.NEXTVAL, 'CONFLICT', 1, l_conf_number, l_conf_name, 'EXAMINER');
                    END IF;
                    
                    IF (p_confname1b != 'NA' AND p_confname1b IS NOT NULL) THEN
                      l_conf_number := SUBSTR(p_confname1b, 1, (INSTR(p_confname1b, '****') - 1));
                      l_conf_name := SUBSTR(p_confname1b, (INSTR(p_confname1b, '****') + 4));
                      l_message := l_unit_name || ' NAME EXAM inserting into name_rule for name_id ' || ni_rec.name_id ||
                                   ' confNumber=' || l_conf_number || ' confName=' || l_conf_name;
                      log_debug(l_message);
                      INSERT INTO name_rule (name_id, name_rule_id, reject_reason_cd, rule_id, conf_number, conf_name, rejected_by)
                         VALUES (ni_rec.name_id, name_rule_seq.NEXTVAL, 'CONFLICT', 1, l_conf_number, l_conf_name, 'EXAMINER');
                    END IF;
                    
                    IF (p_confname1c != 'NA' AND p_confname1c IS NOT NULL) THEN
                      l_conf_number := SUBSTR(p_confname1c, 1, (INSTR(p_confname1c, '****') - 1));
                      l_conf_name := SUBSTR(p_confname1c, (INSTR(p_confname1c, '****') + 4));
                      l_message := l_unit_name || ' NAME EXAM inserting into name_rule for name_id ' || ni_rec.name_id ||
                                   ' confNumber=' || l_conf_number || ' confName=' || l_conf_name;
                      log_debug(l_message);
                      INSERT INTO name_rule (name_id, name_rule_id, reject_reason_cd, rule_id, conf_number, conf_name, rejected_by)
                         VALUES (ni_rec.name_id, name_rule_seq.NEXTVAL, 'CONFLICT', 1, l_conf_number, l_conf_name, 'EXAMINER');
                    END IF;                    
                    
                 ELSIF (ni_rec.choice_number = 2) THEN
                    IF (p_confname2a != 'NA' AND p_confname2a IS NOT NULL) THEN
                      l_conf_number := SUBSTR(p_confname2a, 1, (INSTR(p_confname2a, '****') - 1));
                      l_conf_name := SUBSTR(p_confname2a, (INSTR(p_confname2a, '****') + 4));
                      l_message := l_unit_name || ' NAME EXAM inserting into name_rule for name_id ' || ni_rec.name_id ||
                                   ' confNumber=' || l_conf_number || ' confName=' || l_conf_name;
                      log_debug(l_message);
                      INSERT INTO name_rule (name_id, name_rule_id, reject_reason_cd, rule_id, conf_number, conf_name, rejected_by)
                         VALUES (ni_rec.name_id, name_rule_seq.NEXTVAL, 'CONFLICT', 1, l_conf_number, l_conf_name, 'EXAMINER');
                    END IF;
                    
                    IF (p_confname2b != 'NA' AND p_confname2b IS NOT NULL) THEN
                      l_conf_number := SUBSTR(p_confname2b, 1, (INSTR(p_confname2b, '****') - 1));
                      l_conf_name := SUBSTR(p_confname2b, (INSTR(p_confname2b, '****') + 4));
                      l_message := l_unit_name || ' NAME EXAM inserting into name_rule for name_id ' || ni_rec.name_id ||
                                   ' confNumber=' || l_conf_number || ' confName=' || l_conf_name;
                      log_debug(l_message);
                      INSERT INTO name_rule (name_id, name_rule_id, reject_reason_cd, rule_id, conf_number, conf_name, rejected_by)
                         VALUES (ni_rec.name_id, name_rule_seq.NEXTVAL, 'CONFLICT', 1, l_conf_number, l_conf_name, 'EXAMINER');
                    END IF;
                    
                    IF (p_confname2c != 'NA' AND p_confname2c IS NOT NULL) THEN
                      l_conf_number := SUBSTR(p_confname2c, 1, (INSTR(p_confname2c, '****') - 1));
                      l_conf_name := SUBSTR(p_confname2c, (INSTR(p_confname2c, '****') + 4));
                      l_message := l_unit_name || ' NAME EXAM inserting into name_rule for name_id ' || ni_rec.name_id ||
                                   ' confNumber=' || l_conf_number || ' confName=' || l_conf_name;
                      log_debug(l_message);
                      INSERT INTO name_rule (name_id, name_rule_id, reject_reason_cd, rule_id, conf_number, conf_name, rejected_by)
                         VALUES (ni_rec.name_id, name_rule_seq.NEXTVAL, 'CONFLICT', 1, l_conf_number, l_conf_name, 'EXAMINER');
                    END IF;
                    
                 ELSE
                    IF (p_confname3a != 'NA' AND p_confname3a IS NOT NULL) THEN
                      l_conf_number := SUBSTR(p_confname3a, 1, (INSTR(p_confname3a, '****') - 1));
                      l_conf_name := SUBSTR(p_confname3a, (INSTR(p_confname3a, '****') + 4));
                      l_message := l_unit_name || ' NAME EXAM inserting into name_rule for name_id ' || ni_rec.name_id ||
                                   ' confNumber=' || l_conf_number || ' confName=' || l_conf_name;
                      log_debug(l_message);
                      INSERT INTO name_rule (name_id, name_rule_id, reject_reason_cd, rule_id, conf_number, conf_name, rejected_by)
                         VALUES (ni_rec.name_id, name_rule_seq.NEXTVAL, 'CONFLICT', 1, l_conf_number, l_conf_name, 'EXAMINER');
                    END IF;
                    
                    IF (p_confname3b != 'NA' AND p_confname3b IS NOT NULL) THEN
                      l_conf_number := SUBSTR(p_confname3b, 1, (INSTR(p_confname3b, '****') - 1));
                      l_conf_name := SUBSTR(p_confname3b, (INSTR(p_confname3b, '****') + 4));
                      l_message := l_unit_name || ' NAME EXAM inserting into name_rule for name_id ' || ni_rec.name_id ||
                                   ' confNumber=' || l_conf_number || ' confName=' || l_conf_name;
                      log_debug(l_message);
                      INSERT INTO name_rule (name_id, name_rule_id, reject_reason_cd, rule_id, conf_number, conf_name, rejected_by)
                         VALUES (ni_rec.name_id, name_rule_seq.NEXTVAL, 'CONFLICT', 1, l_conf_number, l_conf_name, 'EXAMINER');
                    END IF;
                    
                    IF (p_confname3c != 'NA' AND p_confname3c IS NOT NULL) THEN
                      l_conf_number := SUBSTR(p_confname3c, 1, (INSTR(p_confname3c, '****') - 1));
                      l_conf_name := SUBSTR(p_confname3c, (INSTR(p_confname3c, '****') + 4));
                      l_message := l_unit_name || ' NAME EXAM inserting into name_rule for name_id ' || ni_rec.name_id ||
                                   ' confNumber=' || l_conf_number || ' confName=' || l_conf_name;
                      log_debug(l_message);
                      INSERT INTO name_rule (name_id, name_rule_id, reject_reason_cd, rule_id, conf_number, conf_name, rejected_by)
                         VALUES (ni_rec.name_id, name_rule_seq.NEXTVAL, 'CONFLICT', 1, l_conf_number, l_conf_name, 'EXAMINER');
                    END IF;
                 END IF;
              END IF;          
              
            END LOOP;
    
    --    consume_request takes care of consuming of name requests. 
    
        IF (p_status IN ('A', 'R')) THEN
          cancel_resubmit(l_request_id, l_event_id);
        END IF;
    
        log_debug(l_unit_name || ' NAME_EXAM committing changes');
        COMMIT; 
        
               
        RETURN l_return;
        
        EXCEPTION
            WHEN OTHERS THEN
              log_debug(l_message || ' FAILED: rolling back changes'); 
              BEGIN
                  ROLLBACK;
                  l_return := 'nro_datapump_pkg: Exception in ' || l_message || '; SQLERRM: ' || SQLERRM;
                  application_log_insert2('nro_datapump_pkg', SYSDATE, 1, string_limit( 'Exception in ' ||
                                 l_message || '; SQLERRM: ' || SQLERRM, 4000));                                 
        
                  RETURN l_return;                    
                  EXCEPTION            
                       WHEN OTHERS THEN   
                       l_return := l_return || ' FAILED: there was issue to insert message into application_log table.';                       
                       log_debug(l_return);                                              
                       RETURN l_return;                 
              END; 
    END name_examination_func;

  
  
  /*
**
** PROCEDURE name_examination
**
** PURPOSE: Update request with the results of a mainframe name examination transaction.
**
** COMMENTS:
** Added to replace the update_name_rule, update_request_state and update_name_rule
** NRO datapump COBRS->NAMESDB events.
**
**
*/
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
                             p_confname3C IN VARCHAR2 DEFAULT 'NA') IS
                             
      l_return   VARCHAR2(32500);                            
      BEGIN                           
         l_return := name_examination_func(p_nr_number, p_status, p_expiry_date, p_consent_flag, p_examiner_id, 
                                         p_choice1, p_choice2, p_choice3, p_exam_comment, p_add_info, p_confname1A, 
                                         p_confname1B, p_confname1C, p_confname2A, p_confname2B, p_confname2C, 
                                         p_confname3A, p_confname3B, p_confname3C );
      END;
        
END nro_datapump_pkg;