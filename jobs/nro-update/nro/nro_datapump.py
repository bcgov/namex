from datetime import timedelta, datetime
from flask import current_app
from pytz import timezone

from namex.models import Name, State
from namex.services.nro.utils import nro_examiner_name


def nro_data_pump_update(nr, ora_cursor, expiry_date):
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
    current_app.logger.debug('processing names for :{}'.format(nr.nrNum))
    for name in nr.names:
        choice = name.choice - 1
        if name.state in [Name.APPROVED, Name.CONDITION]:
            nro_names[choice]['state'] = 'A'
        elif name.state == Name.REJECTED:
            nro_names[choice]['state'] = 'R'
        else:
            nro_names[choice]['state'] = 'NE'

        # some defensive coding here to handle approve/reject/condition where no decision text is available
        # TODO determine if there a business rule requiring APPROVE|REJECTED|CONDITION to have a decision?
        if name.state in [Name.APPROVED, Name.CONDITION, Name.REJECTED]:
            nro_names[choice]['decision'] = '{}****{}'.format(
                nro_names[choice]['state']
                , '  ' if (name.decision_text in [None, '']) else name.decision_text[:1000].encode("ascii","ignore").decode('ascii')
            )

        if name.conflict1:
            nro_names[choice]['conflict1'] = '{}****{}'.format(_clear_NR_num_from_conflict(name.conflict1_num[:10]), name.conflict1[:150])
        if name.conflict2:
            nro_names[choice]['conflict2'] = '{}****{}'.format(_clear_NR_num_from_conflict(name.conflict2_num[:10]), name.conflict2[:150])
        if name.conflict3:
            nro_names[choice]['conflict3'] = '{}****{}'.format(_clear_NR_num_from_conflict(name.conflict3_num[:10]), name.conflict3[:150])

        if name.comment:
            # use the last name comment as the examiner comment, whether that was a rejection or approval
            if name.choice > examiner_comment['choice']:
                examiner_comment['choice'] = name.choice
                examiner_comment['comment'] = name.comment.comment.encode("ascii","ignore").decode('ascii')

    status = 'A' if (nr.stateCd in [State.APPROVED, State.CONDITIONAL]) else 'R'
    consent = 'Y' if (nr.consentFlag == 'Y' or nr.stateCd == State.CONDITIONAL) else 'N'
    current_app.logger.debug('sending {} to NRO'.format(nr.nrNum))
    current_app.logger.debug('nr:{}; stateCd:{}; status: {}; expiry_dt:{}; consent:{}; examiner:{}'
                             .format(nr.nrNum,
                                     nr.stateCd,
                                     status,
                                     expiry_date.strftime('%Y%m%d'),
                                     consent,
                                     nro_examiner_name(nr.activeUser.username)
                                     ))

    # Call the name_examination function to save complete decision data for a single NR
    ret = ora_cursor.callfunc("NRO_DATAPUMP_PKG.name_examination_func",
                              str,
                              [nr.nrNum,  # p_nr_number
                               status,  # p_status
                               expiry_date.strftime('%Y%m%d'),  # p_expiry_date
                               consent,  # p_consent_flag
                               nro_examiner_name(nr.activeUser.username),  # p_examiner_id
                               nro_names[0]['decision'],  # p_choice1
                               nro_names[1]['decision'],  # p_choice2
                               nro_names[2]['decision'],  # p_choice3
                               examiner_comment['comment'],  # p_exam_comment
                               '',  # p_add_info - not used in func anymore
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
    if ret is not None:
        current_app.logger.error('name_examination_func failed, return message: {}'.format(ret))

    current_app.logger.debug('finished sending {} to NRO'.format(nr.nrNum))
    # mark that we've set the record in NRO - which assumes we have legally furnished this to the client.
    # and record the expiry date we sent to NRO
    nr.furnished = 'Y'
    nr.expirationDate = expiry_date

def _clear_NR_num_from_conflict(conflict_num):
    '''
    Remove NR numbers from conflicts when pushing to Oracle - replace with "NR", this is for
    regulatory/privacy reasons.
    :param conflict_num:
    :return: string - conflict_num
    '''
    try:
        if conflict_num[:2] == 'NR': conflict_num = "NR"
    except (TypeError, IndexError) as e:
        pass

    return conflict_num
