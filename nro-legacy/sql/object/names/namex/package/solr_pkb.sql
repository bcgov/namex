CREATE OR REPLACE PACKAGE BODY NAMEX.solr AS
    -- Action Types
    ACTION_UPDATE CONSTANT VARCHAR2(1) := 'U';
    ACTION_DELETE CONSTANT VARCHAR2(1) := 'D';

    -- Status Types
    STATUS_PENDING CONSTANT VARCHAR2(1) := 'P';
    STATUS_ERRORING CONSTANT VARCHAR2(1) := 'E';
    STATUS_COMPLETE CONSTANT VARCHAR2(1) := 'C';
    STATUS_IGNORED CONSTANT VARCHAR2(1) := 'I';

    -- Solr Core Names
    SOLR_CORE_NAMES CONSTANT VARCHAR2(1) := 'N';
    SOLR_CORE_CONFLICTS CONSTANT VARCHAR2(1) := 'C';


    --
    -- Internal function to generate the NR info for Solr.
    --
    FUNCTION generate_json_conflicts(nr_number IN VARCHAR2, action IN VARCHAR2) RETURN VARCHAR2 IS
        content VARCHAR2(4000);
        view_row solr_dataimport_conflicts_vw%ROWTYPE;
    BEGIN
        content := '{ "solr_core": "possible.conflicts", request: ';

        IF action = ACTION_DELETE THEN
            content := content || '{"delete": "' || nr_number || '"}';
        ELSE
            SELECT * INTO view_row FROM solr_dataimport_conflicts_vw WHERE id = nr_number;

            -- Quick and dirty: do this by hand in 11. 12 has JSON stuff.
            content := content || '{"add": {"doc": {' ||
                    '"id": "' || view_row.id || '", ' ||
                    '"name": "' || view_row.name || '", ' ||
                    '"state_type_cd": "' || view_row.state_type_cd || '", ' ||
                    '"source": "' || view_row.source || '" ' ||
                    '} } }';
        END IF;

        content := content || ' }';

        RETURN content;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('solr:gen_conf', SYSDATE(), -1, SQLERRM);
    END;


    --
    -- Internal function to generate the NR info for Solr.
    --
    FUNCTION generate_json_names(nr_number IN VARCHAR2, action IN VARCHAR2) RETURN VARCHAR2 IS
        content VARCHAR2(4000);
        view_row solr_dataimport_names_vw%ROWTYPE;
        CURSOR view_rows IS SELECT * FROM solr_dataimport_names_vw WHERE nr_num = nr_number ORDER BY id;
    BEGIN
        content := '{ "solr_core": "names", request: ';

        IF action = ACTION_DELETE THEN
            -- Relies on Solr ignoring a delete for something that doesn't exist, as we may have fewer than three names.
            content := content || '{"delete": ["' || nr_number || '-1", "' || nr_number || '-2", "' || nr_number ||
                    '-3"]}';
        ELSE
            content := content || '{"add": {"doc": ';

            OPEN view_rows;
            LOOP
                FETCH view_rows INTO view_row;
                EXIT WHEN view_rows%NOTFOUND;

                -- Quick and dirty: do this by hand in 11. 12 has JSON stuff.
                content := content || '{' ||
                        '"id": "' || view_row.id || '", ' ||
                        '"name_instance_id": "' || view_row.name_instance_id || '", ' ||
                        '"choice_number": "' || view_row.choice_number || '", ' ||
                        '"corp_num": "' || view_row.corp_num || '", ' ||
                        '"name": "' || view_row.name || '", ' ||
                        '"nr_num": "' || view_row.nr_num || '", ' ||
                        '"request_id": "' || view_row.request_id || '", ' ||
                        '"submit_count": "' || view_row.submit_count || '", ' ||
                        '"request_type_cd": "' || view_row.request_type_cd || '", ' ||
                        '"name_id": "' || view_row.name_id || '", ' ||
                        '"start_event_id": "' || view_row.start_event_id || '", ' ||
                        '"name_state_type_cd": "' || view_row.name_state_type_cd || '" ' ||
                        '}, ';
            END LOOP;
            CLOSE view_rows;

            content := content || '} }';
        END IF;

        content := content || ' }';

        RETURN content;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('solr:gen_names', SYSDATE(), -1, SQLERRM);
    END;


    --
    -- Internal function to make the call to the Solr-feeder web service. On success, return NULL. If there is a
    -- problem, log it to the application_log table and return the error message received from the web service.
    --
    FUNCTION send_to_solr(nr_number IN VARCHAR2, solr_core IN VARCHAR2, action IN VARCHAR2) RETURN VARCHAR2 IS
        request utl_http.req;
        response utl_http.resp;

        content VARCHAR2(100);
        buffer VARCHAR2(4000);

        error_code INTEGER;
        error_message VARCHAR2(4000);
    BEGIN
        IF solr_core = SOLR_CORE_CONFLICTS THEN
            content := generate_json_conflicts(nr_number, action);
        ELSIF solr_core = SOLR_CORE_NAMES THEN
            content :=  generate_json_names(nr_number, action);
        END IF;

        -- At some point it would make sense to move the ReST stuff out of here and into somewhere re-usable.
        utl_http.set_wallet('file:/dsk01/app/oracle/product/rdbms/11.2.0.4/wallet');
        request := utl_http.begin_request('https://namex-dev.pathfinder.gov.bc.ca/api/v1/feeds/names', 'POST',
                'HTTP/1.1');
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
            application_log_insert('solr.send_to_solr', SYSDATE(), -1, SQLERRM);
    END;


    --
    -- Called from a trigger to queue data that needs to be sent to Solr.
    --
    PROCEDURE load_data IS
        row_transaction_id solr_feeder.transaction_id%type;
        row_transaction_type_cd transaction.transaction_type_cd%type;
        row_event_id transaction.event_id%type;
        row_nr_num solr_feeder.nr_num%type;
        row_state_type_cd request_state.state_type_cd%type;
        approved_count NUMBER;

        CURSOR pending_rows IS SELECT transaction_id FROM name_transaction WHERE status_solr = STATUS_PENDING;
    BEGIN
        OPEN pending_rows;
        LOOP
            FETCH pending_rows INTO row_transaction_id;
            EXIT WHEN pending_rows%NOTFOUND;

            SELECT transaction_type_cd, event_id INTO row_transaction_type_cd, row_event_id FROM transaction WHERE
                    transaction_id = row_transaction_id;

            -- If we don't care about it, mark it as ignored.
            IF row_transaction_type_cd NOT IN ('CONSUME', 'EXPIR', 'HISTORICAL', 'NAME_EXAM') THEN
                UPDATE name_transaction SET status_solr = STATUS_IGNORED WHERE transaction_id = row_transaction_id;
            ELSE
                SELECT nr_num INTO row_nr_num FROM transaction NATURAL JOIN request WHERE transaction_id =
                        row_transaction_id;
                SELECT state_type_cd INTO row_state_type_cd FROM request_state WHERE start_event_id = row_event_id;

                dbms_output.put_line('transaction_id: ' || row_transaction_id || '; nr_num: ' || row_nr_num ||
                        '; state_type_cd: ' || row_state_type_cd);

                IF row_transaction_type_cd = 'NAME_EXAM' AND row_state_type_cd = 'COMPLETED' THEN
                    -- For name examination we need to ensure that there is something the views to update.
                    SELECT COUNT(*) INTO approved_count FROM solr_dataimport_conflicts_vw WHERE id = row_nr_num;
                    dbms_output.put_line('approved count for conflicts: ' || approved_count);

                    IF approved_count > 0 THEN
                        INSERT INTO solr_feeder (id, transaction_id, nr_num, solr_core, action) VALUES
                                (solr_feeder_id_seq.NEXTVAL, row_transaction_id, row_nr_num, SOLR_CORE_CONFLICTS,
                                ACTION_UPDATE);
                    END IF;

                    SELECT COUNT(*) INTO approved_count FROM solr_dataimport_names_vw WHERE nr_num = row_nr_num;
                    dbms_output.put_line('approved count for names: ' || approved_count);

                    IF approved_count > 0 THEN
                        INSERT INTO solr_feeder (id, transaction_id, nr_num, solr_core, action) VALUES
                                (solr_feeder_id_seq.NEXTVAL, row_transaction_id, row_nr_num, SOLR_CORE_NAMES,
                                ACTION_UPDATE);
                    END IF;
                ELSIF row_transaction_type_cd IN ('CONSUME', 'EXPIR', 'HISTORICAL') THEN
                    INSERT INTO solr_feeder (id, transaction_id, nr_num, solr_core, action) VALUES
                            (solr_feeder_id_seq.NEXTVAL, row_transaction_id, row_nr_num, SOLR_CORE_CONFLICTS,
                            ACTION_DELETE);
                END IF;

                UPDATE name_transaction SET status_solr = STATUS_COMPLETE WHERE transaction_id = row_transaction_id;
            END IF;
        END LOOP;
        CLOSE pending_rows;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('solr.load_data', SYSDATE(), -1, SQLERRM);
    END;


    --
    -- Called from a job to send queued changes to Solr.
    --
    PROCEDURE feed_solr IS
        row_id solr_feeder.id%type;
        nr_num request.nr_num%type;
        solr_core_code solr_feeder.solr_core%type;
        solr_core VARCHAR2(18);
        action_code solr_feeder.action%type;
        action VARCHAR2(6);
        update_status VARCHAR2(1);

        CURSOR nr_nums IS SELECT id, nr_num, solr_core, action FROM solr_feeder WHERE status <> STATUS_COMPLETE ORDER BY
                id;

        error_response VARCHAR2(4000);
    BEGIN
        -- Load any data needed for the rows inserted by the trigger.
        load_data();

        OPEN nr_nums;
        LOOP
            FETCH nr_nums INTO row_id, nr_num, solr_core_code, action_code;
            EXIT WHEN nr_nums%NOTFOUND;

            solr_core := CASE solr_core_code
                WHEN SOLR_CORE_CONFLICTS THEN 'possible.conflicts'
                WHEN SOLR_CORE_NAMES THEN 'names'
            END;

            action := CASE action_code
                WHEN ACTION_DELETE THEN 'delete'
                WHEN ACTION_UPDATE THEN 'update'
            END;

            dbms_output.put_line(row_id || ': ' || nr_num || ', ' || solr_core_code || ', ' || action_code);
            error_response := send_to_solr(nr_num, solr_core, action);
            dbms_output.put_line('   -> ' || error_response);

            IF error_response IS NULL THEN
                update_status := STATUS_COMPLETE;
            ELSE
                update_status := STATUS_ERRORING;
            END IF;

            -- This will clear error messages once it finally sends through.
            UPDATE solr_feeder SET status = update_status, send_time = SYSDATE(), send_count = send_count + 1,
                    error_msg = error_response WHERE id = row_id;
        END LOOP;
        CLOSE nr_nums;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('solr.feed_solr', SYSDATE(), -1, SQLERRM);
    END;
END solr;
/
