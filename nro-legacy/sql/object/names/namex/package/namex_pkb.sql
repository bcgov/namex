-- noinspection SqlNoDataSourceInspectionForFile

CREATE OR REPLACE PACKAGE BODY NAMEX.namex AS
    -- Action Types
    ACTION_UPDATE CONSTANT VARCHAR2(1) := 'U';
    ACTION_CREATE CONSTANT VARCHAR2(1) := 'C';

    -- Status Types
    STATUS_PENDING CONSTANT  VARCHAR2(1) := 'P';
    STATUS_ERRORING CONSTANT VARCHAR2(1) := 'E';
    STATUS_COMPLETE CONSTANT VARCHAR2(1) := 'C';
    STATUS_IGNORED CONSTANT  VARCHAR2(1) := 'I';

    --
    -- Internal function to make the call to the Solr-feeder web service. On success, return NULL. If there is a
    -- problem, log it to the application_log table and return the error message received from the web service.
    --
    FUNCTION send_to_namex(nr_number IN VARCHAR2, action IN VARCHAR2) RETURN VARCHAR2 IS
        oracle_wallet configuration.value%TYPE;
        destination_url configuration.value%TYPE;

        request utl_http.req;
        response utl_http.resp;

        content VARCHAR2(4000);
        buffer VARCHAR2(4000);
        http_verb VARCHAR2(10);

        error_code INTEGER;
        error_message VARCHAR2(4000);
    BEGIN
        -- configuration table lifted from globaldb. We should have a function for fetching these, and we should only
        -- call it with "NAMEX_FEEDER", the function should grab the GLOBAL value if the name doesn't exist for the
        -- application.
        SELECT value INTO oracle_wallet FROM configuration
        WHERE application = 'GLOBAL' AND name = 'oracle_wallet';
        SELECT value INTO destination_url FROM configuration
        WHERE application = 'NAMEX_FEEDER' AND name = 'destination_url';

        -- determine if this is a POST or PUT
        IF action = ACTION_CREATE THEN
            http_verb := 'POST';
        ELSE
            http_verb := 'PUT';
        END IF;

        -- create the very small json
        content := '{"nameRequest": "' || nr_number || '"}';

        -- At some point it would make sense to move the ReST stuff out of here and into somewhere re-usable.
        utl_http.set_wallet(oracle_wallet);
        request := utl_http.begin_request(destination_url, http_verb, 'HTTP/1.1');
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
        application_log_insert('namex.send_to_namex', SYSDATE(), response.status_code, error_message);

        RETURN error_message;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('namex.send_to_namex', SYSDATE(), -1, SQLERRM);
    END;


    --
    -- Called from a trigger to queue data that needs to be sent to NameX.
    --
    PROCEDURE load_data IS
        row_transaction_id namex_feeder.transaction_id%type;
        row_transaction_type_cd transaction.transaction_type_cd%type;
        row_event_id transaction.event_id%type;
        row_nr_num namex_feeder.nr_num%type;
        row_state_type_cd request_state.state_type_cd%type;
        approved_count NUMBER;
        status CHAR(1);
        row_action CHAR(1);

        CURSOR pending_rows IS SELECT transaction_id FROM name_transaction WHERE status_namex = STATUS_PENDING ORDER BY
                transaction_id;
    BEGIN
        OPEN pending_rows;
        LOOP
            FETCH pending_rows INTO row_transaction_id;
            EXIT WHEN pending_rows%NOTFOUND;

            SELECT transaction_type_cd, event_id INTO row_transaction_type_cd, row_event_id FROM transaction WHERE
                    transaction_id = row_transaction_id;

            -- If we don't care about it, mark it as ignored.
            status := STATUS_IGNORED;

            -- get the current state, if it's not 'C' or 'D' we're done
            BEGIN
                SELECT state_type_cd INTO row_state_type_cd FROM request_state WHERE start_event_id = row_event_id AND
                        state_type_cd in ('C', 'D');
            EXCEPTION
                WHEN NO_DATA_FOUND THEN
                    row_state_type_cd := NULL;
            END;

			IF (row_state_type_cd IN ('C', 'D')
			    AND 
			    row_transaction_type_cd IN 
			         ('ADMIN', 'NRREQ', 'RESUBMIT', 'CANCL', 'MODIF', 'CORRT', 'UPDPR')
			   )
			  -- (row_state_type_cd = 'COMPLETED' and row_transaction_type_cd = 'EXTEND')
			THEN
				SELECT nr_num INTO row_nr_num FROM transaction NATURAL JOIN request WHERE transaction_id =
						row_transaction_id;

				dbms_output.put_line('transaction_id: ' || row_transaction_id ||
						'; nr_num: ' || row_nr_num ||
						'; state_type_cd: ' || row_state_type_cd ||
						'; row_transaction_type_cd: '|| row_transaction_type_cd);

				IF row_transaction_type_cd in ('NRREQ', 'RESUBMIT') THEN
					row_action := ACTION_CREATE;
				ELSE
					row_action := ACTION_UPDATE;
				END IF;

				INSERT INTO namex_feeder (id, transaction_id, nr_num, action)
				VALUES (namex_feeder_id_seq.NEXTVAL, row_transaction_id, row_nr_num, row_action);
				status := STATUS_COMPLETE;


            END IF;

            UPDATE name_transaction SET status_namex = status WHERE transaction_id = row_transaction_id;
        END LOOP;
        CLOSE pending_rows;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('namex.load_data', SYSDATE(), -1, SQLERRM);
    END;


    --
    -- Called from a job to send queued changes to Solr.
    --
    PROCEDURE feed_namex IS
        CURSOR namex_feeder IS SELECT * FROM namex_feeder WHERE status <> STATUS_COMPLETE ORDER BY id;
        namex_feeder_row namex_feeder%ROWTYPE;

        error_response VARCHAR2(4000);
        update_status VARCHAR2(1);
    BEGIN
        -- Load any data needed for the rows inserted by the trigger.
        load_data();

        OPEN namex_feeder;
        LOOP
            FETCH namex_feeder INTO namex_feeder_row;
            EXIT WHEN namex_feeder%NOTFOUND;

            dbms_output.put_line(namex_feeder_row.id
                                || ': ' || namex_feeder_row.nr_num 
                                || ', ' || namex_feeder_row.action);

            -- send the message
            error_response := send_to_namex(namex_feeder_row.nr_num, namex_feeder_row.action);
            dbms_output.put_line('   -> ' || error_response);

            IF error_response IS NULL THEN
                update_status := STATUS_COMPLETE;
            ELSE
                update_status := STATUS_ERRORING;
            END IF;

            -- This will clear error messages once it finally sends through.
            UPDATE namex_feeder SET status = update_status, send_time = SYSDATE(), send_count = send_count + 1,
                    error_msg = error_response WHERE id = namex_feeder_row.id;
            COMMIT;
        END LOOP;
        CLOSE namex_feeder;
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('namex.feed_namex', SYSDATE(), -1, SQLERRM);
    END;
END namex;
/
