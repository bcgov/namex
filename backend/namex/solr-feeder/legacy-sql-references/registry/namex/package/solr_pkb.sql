-- noinspection SqlNoDataSourceInspectionForFile

CREATE OR REPLACE PACKAGE BODY NAMEX.solr AS
    -- Action Types
    ACTION_UPDATE CONSTANT VARCHAR2(1) := 'U';
    ACTION_DELETE CONSTANT VARCHAR2(1) := 'D';
    ACTION_SYNC CONSTANT VARCHAR2(1) := 'S';

    -- Status Types
    STATUS_PENDING CONSTANT VARCHAR2(1) := 'P';
    STATUS_ERRORING CONSTANT VARCHAR2(1) := 'E';
    STATUS_COMPLETE CONSTANT VARCHAR2(1) := 'C';
    STATUS_IGNORED CONSTANT VARCHAR2(1) := 'I';


    --
    -- Internal function to generate the info for Solr.
    --
    FUNCTION generate_json_conflicts(corp_num IN VARCHAR2, action IN VARCHAR2) RETURN VARCHAR2 IS
        content VARCHAR2(4000);
        view_row solr_dataimport_conflicts_vw%ROWTYPE;
    BEGIN
        content := '{ "solr_core": "possible.conflicts", "request": "{';

        IF action = ACTION_DELETE THEN
            content := content || '\"delete\": \"' || corp_num || '\", ';
        ELSE
            SELECT * INTO view_row FROM solr_dataimport_conflicts_vw WHERE id = corp_num;

            -- Quick and dirty: do this by hand in 11. 12 has JSON stuff.
            content := content || '\"add\": {\"doc\": {' ||
                    '\"id\": \"' || view_row.id || '\", ' ||
                    '\"name\": \"' || REPLACE(REPLACE(view_row.name, '\', '\\\\'), '"', '\\\"') || '\", ' ||
                    '\"state_type_cd\": \"' || view_row.state_type_cd || '\", ' ||
                    '\"source\": \"' || view_row.source || '\", ' ||
					'\"start_date\": \"' || to_char(view_row.start_date,'YYYY-MM-DD"T"HH24:MI:SS"Z"') || '\", ' ||
					'\"jurisdiction\": \"' || view_row.jurisdiction || '\" ' ||
                    '} }, ';
        END IF;

        content := content || '\"commit\": {} }" }';

        RETURN content;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            if SQLERRM <> 'ORA-01403: no data found' then
               application_log_insert('solr:gen_conf', SYSDATE(), -1, SQLERRM);
            end if;

            RAISE;
    END;


    --
    -- Internal function to make the call to the Solr-feeder web service. On success, return NULL. If there is a
    -- problem, log it to the application_log table and return the error message received from the web service.
    --
    FUNCTION send_to_solr(nr_number IN VARCHAR2, action IN VARCHAR2) RETURN VARCHAR2 IS
        oracle_wallet configuration.value%TYPE;
        destination_url configuration.value%TYPE;

        request utl_http.req;
        response utl_http.resp;

        content VARCHAR2(4000);
        buffer VARCHAR2(4000);

        corp_typ_cd corp_type.corp_typ_cd%TYPE;

        error_code INTEGER;
        error_message VARCHAR2(4000);
    BEGIN
        -- configuration table lifted from globaldb. We should have a function for fetching these, and we should only
        -- call it with "SOLR_FEEDER", the function should grab the GLOBAL value if the name doesn't exist for the
        -- application.
        SELECT value INTO oracle_wallet FROM configuration WHERE application = 'GLOBAL' AND name = 'oracle_wallet';
        SELECT value INTO destination_url FROM configuration WHERE application = 'SOLR_FEEDER' AND name =
                'destination_url';

        IF action = ACTION_SYNC THEN
            -- NOTE: nr_number == corp_num in this case
            SELECT corp_typ_cd INTO corp_typ_cd FROM corp_type NATURAL JOIN corporation WHERE corp_num = nr_number;
            -- NOTE: CPs/BENs are only updated in CPRD via LEAR which already triggers a search update and the CPRD data can be out of date so skip.
            -- SP/GPs are in LEAR but can still get updates in CPRD via a backdoor flow so they are still enabled here.
            IF corp_typ_cd NOT IN ('CP','BEN') THEN
                content := '{ "solr_core": "search", "identifier": "' || nr_number || '", "legalType": "' || corp_typ_cd || '"}';
            ELSE
                RETURN NULL;
            END IF;
        ELSE
            content := generate_json_conflicts(nr_number, action);
        END IF;

        -- At some point it would make sense to move the ReST stuff out of here and into somewhere re-usable.
        utl_http.set_wallet(oracle_wallet);
        request := utl_http.begin_request(destination_url, 'POST', 'HTTP/1.1');
        utl_http.set_header(request, 'Content-Type', 'application/json');
        utl_http.set_header(request, 'Content-Length', LENGTH(content));
        utl_http.write_text(request, content);

        response := utl_http.get_response(request);

        dbms_output.put_line('Response ' || response.status_code || ' (' || response.reason_phrase || ')');

        -- Success.
        IF response.status_code = 200 THEN
            utl_http.end_response(response);

            RETURN NULL;
        END IF;

        -- Failure.
        error_message := 'HTTP ' || response.status_code || ': ';
        BEGIN
            -- Collapse the response into a single line. Note that the response could be many lines of 4000 characters
            -- each, so if it's a huge stack trace then it won't fit into the buffer. Make sure that we don't exceed the
            -- length of the buffer, at the cost of losing the end of large error messages.

            LOOP
                utl_http.read_line(response, buffer);
                error_code := response.status_code;
                error_message := error_message ||
                        SUBSTR(TRIM(REPLACE(buffer, CHR(10))), 0, 4000 - LENGTH(error_message));
            END LOOP;
        EXCEPTION
            WHEN utl_http.end_of_body THEN
                utl_http.end_response(response);
        END;

        -- Report on the error.
        dbms_output.put_line(response.status_code || ': ' || error_message);
        application_log_insert('solr.send_to_solr', SYSDATE(), response.status_code, error_message);

        RETURN error_message;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            if SQLERRM <> 'ORA-01403: no data found' then
               application_log_insert('solr.send_to_solr', SYSDATE(), -1, SQLERRM);
            end if;

            return SQLERRM;
    END;


    --
    -- Called from a trigger to queue name data that needs to be sent to Solr.
    --
    PROCEDURE load_name_data IS
        CURSOR pending_rows IS SELECT * FROM triggered_corp_name WHERE status_solr = STATUS_PENDING ORDER BY id;
        triggered_name triggered_corp_name%ROWTYPE;
        corp_class corp_type.corp_class%TYPE;
    BEGIN
        OPEN pending_rows;
        LOOP
            FETCH pending_rows INTO triggered_name;
            EXIT WHEN pending_rows%NOTFOUND;

            SELECT corp_class INTO corp_class FROM corp_type NATURAL JOIN corporation WHERE corp_num =
                    triggered_name.corp_num;

            -- If we don't care about it, mark it as ignored.
            IF corp_class NOT IN ('BC', 'OT', 'SOC', 'XPRO') THEN
                UPDATE triggered_corp_name SET status_solr = STATUS_IGNORED WHERE id = triggered_name.id;
            ELSE
                INSERT INTO solr_feeder (id, transaction_id, corp_num, action) VALUES (solr_feeder_id_seq.NEXTVAL,
                        triggered_name.id, triggered_name.corp_num, ACTION_UPDATE);

                UPDATE triggered_corp_name SET status_solr = STATUS_COMPLETE WHERE id = triggered_name.id;
            END IF;
        END LOOP;
        CLOSE pending_rows;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('solr.load_name_data', SYSDATE(), -1, SQLERRM);
    END;


    --
    -- Called from a trigger to queue state data that needs to be sent to Solr.
    --
    PROCEDURE load_state_data IS
        CURSOR pending_rows IS SELECT * FROM triggered_corp_state WHERE status_solr = STATUS_PENDING ORDER BY id;
        triggered_state triggered_corp_state%ROWTYPE;
        corp_class corp_type.corp_class%TYPE;
        op_state_typ_cd corp_op_state.op_state_typ_cd%TYPE;
    BEGIN
        OPEN pending_rows;
        LOOP
            FETCH pending_rows INTO triggered_state;
            EXIT WHEN pending_rows%NOTFOUND;

            SELECT corp_class INTO corp_class FROM corp_type NATURAL JOIN corporation WHERE corp_num =
                    triggered_state.corp_num;

            -- If we don't care about it, mark it as ignored.
            IF corp_class NOT IN ('BC', 'OT', 'SOC', 'XPRO') THEN
                UPDATE triggered_corp_state SET status_solr = STATUS_IGNORED WHERE id = triggered_state.id;
            ELSE
                SELECT op_state_typ_cd INTO op_state_typ_cd FROM corp_op_state NATURAL JOIN corp_state WHERE corp_num =
                        triggered_state.corp_num AND end_event_id IS NULL;

                IF op_state_typ_cd = 'ACT' THEN
                    INSERT INTO solr_feeder (id, transaction_id, corp_num, action) VALUES (solr_feeder_id_seq.NEXTVAL,
                            triggered_state.id, triggered_state.corp_num, ACTION_UPDATE);
                ELSE
                    INSERT INTO solr_feeder (id, transaction_id, corp_num, action) VALUES (solr_feeder_id_seq.NEXTVAL,
                            triggered_state.id, triggered_state.corp_num, ACTION_DELETE);
                END IF;

                UPDATE triggered_corp_state SET status_solr = STATUS_COMPLETE WHERE id = triggered_state.id;
            END IF;
        END LOOP;
        CLOSE pending_rows;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('solr.load_state_data', SYSDATE(), -1, SQLERRM);
    END;


    --
    -- Called from a trigger to queue corporation data that needs to be sent to Search Solr.
    --
    PROCEDURE load_corporation_data IS
        CURSOR pending_rows IS SELECT max(id) as id, corp_num, status_solr FROM triggered_corporation WHERE status_solr = STATUS_PENDING GROUP BY corp_num, status_solr ORDER BY id ASC;
        triggered_corp triggered_corporation%ROWTYPE;
    BEGIN
        OPEN pending_rows;
        LOOP
            FETCH pending_rows INTO triggered_corp;
            EXIT WHEN pending_rows%NOTFOUND;

            INSERT INTO solr_feeder (id, transaction_id, corp_num, action) VALUES (solr_feeder_id_seq.NEXTVAL,
                    triggered_corp.id, triggered_corp.corp_num, ACTION_SYNC);

            UPDATE triggered_corporation SET status_solr = STATUS_COMPLETE WHERE id = triggered_corporation.id;
        END LOOP;
        CLOSE pending_rows;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('solr.load_corporation_data', SYSDATE(), -1, SQLERRM);
    END;


    --
    -- Called from a job to send queued changes to Solr.
    --
    PROCEDURE feed_solr IS
        CURSOR solr_feeder IS SELECT * FROM solr_feeder WHERE status <> STATUS_COMPLETE and status <> STATUS_IGNORED AND send_count < 60 ORDER BY id;
        solr_feeder_row solr_feeder%ROWTYPE;

        error_response VARCHAR2(4000);
        update_status VARCHAR2(1);
    BEGIN
        -- Load any data needed for the rows inserted by the trigger.
        load_name_data();
        load_state_data();
        load_corporation_data();  -- for business/director search sync

        OPEN solr_feeder;
        LOOP
            FETCH solr_feeder INTO solr_feeder_row;
            EXIT WHEN solr_feeder%NOTFOUND;

            dbms_output.put_line(solr_feeder_row.id || ': ' || solr_feeder_row.corp_num || ', ' ||
                    solr_feeder_row.action);
            error_response := send_to_solr(solr_feeder_row.corp_num, solr_feeder_row.action);
            dbms_output.put_line('   -> ' || error_response);

            IF error_response IS NULL THEN
                update_status := STATUS_COMPLETE;
            ELSE
                update_status := STATUS_ERRORING;
            END IF;

            -- This will clear error messages once it finally sends through.
            UPDATE solr_feeder SET status = update_status, send_time = SYSDATE(), send_count = send_count + 1,
                    error_msg = error_response WHERE id = solr_feeder_row.id;
            COMMIT;
        END LOOP;
        CLOSE solr_feeder;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('solr.feed_solr', SYSDATE(), -1, SQLERRM);
    END;
END solr;
/
