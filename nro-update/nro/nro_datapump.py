from datetime import timedelta

from namex.models import Name, State


def nro_data_pump_update(nr, ora_cursor, expires_days=60):

    expiry_date = nr.lastUpdate + timedelta(days=expires_days)

    # initialize array of derived values to use in the stored proc
    names = [
        {'state': None, 'decision': None, 'conflict1': None, 'conflict2': None, 'conflict3': None},
        {'state': None, 'decision': None, 'conflict1': None, 'conflict2': None, 'conflict3': None},
        {'state': None, 'decision': None, 'conflict1': None, 'conflict2': None, 'conflict3': None}
    ]
    for name in nr.names.all():
        choice = name.choice - 1
        if name.state in [Name.APPROVED, name.CONDITION]:
            names[choice]['state'] = 'A'
        elif name.state == Name.REJECTED:
            names[choice]['state'] = 'R'
        else:
            names[choice]['state'] = 'NE'

        decision_text = ''
        if name.state in [Name.APPROVED, name.CONDITION]:
            names[choice]['decision'] = '{}****{}'.format(name.state, name.decision_text[:1000])

        if name.conflict1:
            names[choice]['conflict1'] = '{}****{}'.format(name.conflict1_num[:10], name.conflict1[:150])

        if name.conflict2:
            names[choice]['conflict2'] = '{}****{}'.format(name.conflict2_num[:10], name.conflict2[:150])

        if name.conflict3:
            names[choice]['conflict3'] = '{}****{}'.format(name.conflict3_num[:10], name.conflict3[:150])

    ### Call the name_examination procedure to save complete decision data for a single NR
    ora_cursor.callproc("NRO_DATAPUMP_PKG.name_examination",
                        [nr.nrNum,  # p_nr_number
                         'A' if (nr.stateCd in [State.APPROVED, State.CONDITIONAL]) else 'R',  # p_status
                         expiry_date.strftime('%Y%m%d'),  # p_expiry_date
                         'Y' if (nr.consentFlag in ['Y', State.CONDITIONAL]) else 'N',  # p_consent_flag
                         nr.activeUser.username[:7],  # p_examiner_id
                         names[0]['decision'],  # p_choice1
                         names[1]['decision'],  # p_choice2
                         names[2]['decision'],  # p_choice3
                         '',  # p_exam_comment TODO
                         '',  # p_add_info - not used in proc anymore
                         names[0]['conflict1'],  # p_confname1A
                         names[0]['conflict2'],  # p_confname1B
                         names[0]['conflict3'],  # p_confname1C
                         names[1]['conflict1'],  # p_confname2A
                         names[1]['conflict2'],  # p_confname2B
                         names[1]['conflict3'],  # p_confname2C
                         names[2]['conflict1'],  # p_confname3A
                         names[2]['conflict2'],  # p_confname3B
                         names[2]['conflict3'],  # p_confname3C
                         ]
                        )
    # mark that we've set the record in NRO - which assumes we have legally furnished this to the client.
    nr.furnished = 'Y'
    nr.expirationDate = expiry_date
