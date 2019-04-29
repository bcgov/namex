-- noinspection SqlNoDataSourceInspectionForFile

CREATE OR REPLACE PACKAGE BODY NAMEX.namex AS
    -- Action Types
    ACTION_UPDATE CONSTANT VARCHAR2(1) := 'U';
    ACTION_CREATE CONSTANT VARCHAR2(1) := 'C';
    ACTION_CANCEL CONSTANT VARCHAR2(1) := 'X';

    -- Status Types
    STATUS_PENDING CONSTANT  VARCHAR2(1) := 'P';
    STATUS_ERRORING CONSTANT VARCHAR2(1) := 'E';
    STATUS_COMPLETE CONSTANT VARCHAR2(1) := 'C';
    STATUS_IGNORED CONSTANT  VARCHAR2(1) := 'I';

    --
    -- Called from a job to queue data that needs to be sent to NameX.
    --
    PROCEDURE queue_data_for_namex IS
        row_transaction_id namex_feeder.transaction_id%type;
        row_transaction_type_cd transaction.transaction_type_cd%type;
        row_request_id transaction.request_id%type;
        row_event_id transaction.event_id%type;
        row_nr_num namex_feeder.nr_num%type;
        row_state_type_cd request_state.state_type_cd%type;
        approved_count NUMBER;
        status CHAR(1);
        row_action CHAR(1);

        CURSOR pending_rows IS 
        SELECT transaction_id 
        FROM name_transaction 
        WHERE status_namex = STATUS_PENDING
        ORDER BY transaction_id;
        
    BEGIN
        OPEN pending_rows;
        LOOP
            FETCH pending_rows INTO row_transaction_id;
            EXIT WHEN pending_rows%NOTFOUND;

            SELECT transaction_type_cd, request_id, event_id
            INTO row_transaction_type_cd, row_request_id, row_event_id
            FROM transaction 
            WHERE transaction_id = row_transaction_id;

            -- If we don't care about it, mark it as ignored.
            status := STATUS_IGNORED;

            -- get the current state, if it's not 'C' or 'D' we're done
            BEGIN
                SELECT state_type_cd 
                INTO row_state_type_cd 
                FROM request_state 
                WHERE request_id = row_request_id
                AND end_event_id is NULL
                AND state_type_cd in ('C', 'D', 'COMPLETED');
                
            EXCEPTION
                WHEN NO_DATA_FOUND THEN
                    row_state_type_cd := NULL;
            END;

			IF ((row_state_type_cd IN ('C', 'D')
			    AND
			    row_transaction_type_cd IN
			         ('ADMIN', 'NRREQ', 'RESUBMIT', 'CANCL', 'MODIF', 'CORRT', 'UPDPR')
			   ) OR (
			    row_state_type_cd IN ('COMPLETED') AND row_transaction_type_cd IN ('CONSUME')
			    ))
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
					
				ELSIF row_transaction_type_cd in ('CANCL') THEN
					row_action := ACTION_CANCEL;
					
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

END namex;
/
