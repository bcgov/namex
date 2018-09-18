from datetime import timedelta

from namex.models import Name, State
from namex.services.nro.utils import nro_examiner_name


def nro_data_pump_update(nr, ora_cursor, expires_days=60):

    expiry_date = nr.lastUpdate + timedelta(days=expires_days)

    # init dict for examiner comment data, populated below in loop through names
    examiner_comment = {
        'choice': 0,
        'comment': None,
    }

    # initialize array of derived values to use in the stored proc
    nro_names = [
        {'state': None, 'decision': None, 'conflict1': None, 'conflict2': None, 'conflict3': None},
        {'state': None, 'decision': None, 'conflict1': None, 'conflict2': None, 'conflict3': None},
        {'state': None, 'decision': None, 'conflict1': None, 'conflict2': None, 'conflict3': None}
    ]
    for name in nr.names.all():
        choice = name.choice - 1
        if name.state in [Name.APPROVED, name.CONDITION]:
            nro_names[choice]['state'] = 'A'
        elif name.state == Name.REJECTED:
            nro_names[choice]['state'] = 'R'
        else:
            nro_names[choice]['state'] = 'NE'

        decision_text = ''
        # some defensive coding here to handle approve/reject/condition where no decision text is available
        # TODO determine if there a business rule requiring APPROVE|REJECTED|CONDITION to have a decision?
        if name.state in [Name.APPROVED, Name.CONDITION, Name.REJECTED]:
            nro_names[choice]['decision'] = '{}****{}'.format(
                nro_names[choice]['state']
                , '  ' if (name.decision_text is None) else name.decision_text[:1000]
            )

        if name.conflict1:
            nro_names[choice]['conflict1'] = '{}****{}'.format(name.conflict1_num[:10], name.conflict1[:150])
        if name.conflict2:
            nro_names[choice]['conflict2'] = '{}****{}'.format(name.conflict2_num[:10], name.conflict2[:150])
        if name.conflict3:
            nro_names[choice]['conflict3'] = '{}****{}'.format(name.conflict3_num[:10], name.conflict3[:150])

        if name.comment:
            # use the last name comment as the examiner comment, whether that was a rejection or approval
            if name.choice > examiner_comment['choice']:
                examiner_comment['choice'] = name.choice
                examiner_comment['comment'] = name.comment.comment

    # # Call the name_examination procedure to save complete decision data for a single NR
    ora_cursor.callproc("NRO_DATAPUMP_PKG.name_examination",
                        [nr.nrNum,  # p_nr_number
                         'A' if (nr.stateCd in [State.APPROVED, State.CONDITIONAL]) else 'R',  # p_status
                         expiry_date.strftime('%Y%m%d'),  # p_expiry_date
                         'Y' if (nr.consentFlag == 'Y' or nr.stateCd == State.CONDITIONAL) else 'N',  # p_consent_flag
                         nro_examiner_name(nr.activeUser.username),  # p_examiner_id
                         nro_names[0]['decision'],  # p_choice1
                         nro_names[1]['decision'],  # p_choice2
                         nro_names[2]['decision'],  # p_choice3
                         examiner_comment['comment'],  # p_exam_comment
                         '',  # p_add_info - not used in proc anymore
                         nro_names[0]['conflict1'],  # p_confname1A
                         nro_names[0]['conflict2'],  # p_confname1B
                         nro_names[0]['conflict3'],  # p_confname1C
                         nro_names[1]['conflict1'],  # p_confname2A
                         nro_names[1]['conflict2'],  # p_confname2B
                         nro_names[1]['conflict3'],  # p_confname2C
                         nro_names[2]['conflict1'],  # p_confname3A
                         nro_names[2]['conflict2'],  # p_confname3B
                         nro_names[2]['conflict3'],  # p_confname3C
                         ]
                        )
    # mark that we've set the record in NRO - which assumes we have legally furnished this to the client.
    # and record the expiry date we sent to NRO
    nr.furnished = 'Y'
    nr.expirationDate = expiry_date
