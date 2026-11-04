// ABC PLUMBING
const testData = [
  {
    'test': 1,
    'name': 'ABC PLUMBING',
    'corrected': 'ABC PLUMBING INCORPORATED',
    'analysisJSON': {
      'header': 'Further Action Required',
      'status': 'fa',
      'issues': [
        {
          'line1': 'Too similar to an existing name in queue.',
          'issue_type': 'queue_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INC.',
              'date': '2020-10-13',
              'start_date': '2020-07-21T19:57:00+00:00',
              'id': 'NR 8479118',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 2',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'Too similar to an existing name.',
          'issue_type': 'corp_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INCORPORATED',
              'date': '2020-10-13',
              'start_date': '2020-10-02T01:36:35.997287+00:00',
              'id': 'NR 9541590',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'send_to_examiner',
              'header': 'Option 2',
              'line1': 'You can choose to submit this name for examination. Please check wait times at the top of the' +
              ' screen.',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 3',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'Further Action. A designation is required. Please select one from Option 1 below.',
          'designations': [
            'INCORPORATED',
            'CORPORATION',
            'LIMITED',
            'CORP.',
            'INC.',
            'LTD.',
            'INCORPOREE',
            'LIMITEE',
            'LTEE'
          ],
          'issue_type': 'designation_non_existent',
          'show_next_button': false,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'add_designation',
              'header': 'Option 1',
              'line1': 'Please select a designation from one of the following:',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        }
      ]
    }
  },
  {
    'test': 2,
    'name': 'ABC LTD. PLUMBING',
    'corrected': 'ABC PLUMBING LTD.',
    'analysisJSON': {
      'header': 'Further Action Required',
      'status': 'fa',
      'issues': [
        {
          'line1': 'Too similar to an existing name in queue.',
          'issue_type': 'queue_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INC.',
              'date': '2020-10-13',
              'start_date': '2020-07-21T19:57:00+00:00',
              'id': 'NR 8479118',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 2',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'Too similar to an existing name.',
          'issue_type': 'corp_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INCORPORATED',
              'date': '2020-10-13',
              'start_date': '2020-10-02T01:36:35.997287+00:00',
              'id': 'NR 9541590',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'send_to_examiner',
              'header': 'Option 2',
              'line1': 'You can choose to submit this name for examination. Please check wait times at the top of the' +
              ' screen.',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 3',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'The \u003cb\u003eLTD.\u003c/b\u003e designation(s) must be at the end of the name.',
          'issue_type': 'designation_misplaced',
          'show_next_button': false,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'change designation at the end',
              'header': 'Option 1',
              'line1': 'Change designation order to the end of the name.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': [
            {
              'type': 'highlight',
              'word': 'LTD.',
              'index': 4
            }
          ]
        }
      ]
    }
  },
  {
    'test': 3,
    'name': 'ABC L.L.C. PLUMBING',
    'corrected': 'ABC PLUMBING INCORPORATED',
    'analysisJSON': {
      'header': 'Further Action Required',
      'status': 'fa',
      'issues': [
        {
          'line1': 'Too similar to an existing name in queue.',
          'issue_type': 'queue_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INC.',
              'date': '2020-10-13',
              'start_date': '2020-07-21T19:57:00+00:00',
              'id': 'NR 8479118',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 2',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'Too similar to an existing name.',
          'issue_type': 'corp_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INCORPORATED',
              'date': '2020-10-13',
              'start_date': '2020-10-02T01:36:35.997287+00:00',
              'id': 'NR 9541590',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'send_to_examiner',
              'header': 'Option 2',
              'line1': 'You can choose to submit this name for examination. Please check wait times at the top of the' +
              ' screen.',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 3',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'The \u003cb\u003eL.L.C.\u003c/b\u003e designation(s) cannot be used with selected entity type of' +
          ' Corporation\u003c/b\u003e.',
          'designations': [
            'INCORPORATED',
            'CORPORATION',
            'LIMITED',
            'CORP.',
            'INC.',
            'LTD.',
            'INCORPOREE',
            'LIMITEE',
            'LTEE'
          ],
          'issue_type': 'designation_mismatch',
          'show_next_button': false,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'replace_designation',
              'header': 'Option 1',
              'line1': 'Change the designation from to one of the following:',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'change_entity_type',
              'header': 'Option 2',
              'line1': 'The designation you have selected is not appropriate for this entity type. You can choose to' +
              ' select a different type by pressing the \u0027RESTART and CHANGE TYPE\u0027 button.',
              'line2': '',
              'label': 'Change $entity_type to \u003cb\u003eINCORPORATED, CORPORATION, LIMITED, CORP., INC., LTD.,' +
              ' INCORPOREE, LIMITEE, LTEE\u003c/b\u003e'
            }
          ],
          'name_actions': [
            {
              'type': 'highlight',
              'word': 'L.L.C.',
              'index': 4
            }
          ]
        }
      ]
    }
  },
  {
    'test': 4,
    'name': 'ABC PLUMBING CO-OP',
    'corrected': 'ABC PLUMBING INCORPORATED',
    'analysisJSON': {
      'header': 'Further Action Required',
      'status': 'fa',
      'issues': [
        {
          'line1': 'Too similar to an existing name in queue.',
          'issue_type': 'queue_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING',
              'date': '2020-10-14',
              'start_date': '2020-07-14T23:38:10+00:00',
              'id': 'NR 9110602',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 2',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'Too similar to an existing name.',
          'issue_type': 'corp_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INCORPORATED',
              'date': '2020-10-14',
              'start_date': '2020-10-02T01:36:35.997287+00:00',
              'id': 'NR 9541590',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'send_to_examiner',
              'header': 'Option 2',
              'line1': 'You can choose to submit this name for examination. Please check wait times at the top of the' +
              ' screen.',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 3',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'The \u003cb\u003eCOOP\u003c/b\u003e designation(s) cannot be used with selected entity type of' +
          ' Corporation\u003c/b\u003e.',
          'designations': [
            'INCORPORATED',
            'CORPORATION',
            'LIMITED',
            'CORP.',
            'INC.',
            'LTD.',
            'INCORPOREE',
            'LIMITEE',
            'LTEE'
          ],
          'issue_type': 'designation_mismatch',
          'show_next_button': false,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'replace_designation',
              'header': 'Option 1',
              'line1': 'Change the designation from to one of the following:',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'change_entity_type',
              'header': 'Option 2',
              'line1': 'The designation you have selected is not appropriate for this entity type. You can choose to' +
              ' select a different type by pressing the \u0027RESTART and CHANGE TYPE\u0027 button.',
              'line2': '',
              'label': 'Change $entity_type to \u003cb\u003eINCORPORATED, CORPORATION, LIMITED, CORP., INC., LTD.,' +
              ' INCORPOREE, LIMITEE, LTEE\u003c/b\u003e'
            }
          ],
          'name_actions': []
        }
      ]
    }
  },
  {
    'test': 5,
    'name': 'ABC PLUMBING COOP L.L.C.',
    'corrected': 'ABC PLUMBING INCORPORATED',
    'analysisJSON': {
      'header': 'Further Action Required',
      'status': 'fa',
      'issues': [
        {
          'line1': 'Too similar to an existing name in queue.',
          'issue_type': 'queue_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INC.',
              'date': '2020-10-14',
              'start_date': '2020-07-21T19:57:00+00:00',
              'id': 'NR 8479118',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 2',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'Too similar to an existing name.',
          'issue_type': 'corp_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INCORPORATED',
              'date': '2020-10-14',
              'start_date': '2020-10-02T01:36:35.997287+00:00',
              'id': 'NR 9541590',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'send_to_examiner',
              'header': 'Option 2',
              'line1': 'You can choose to submit this name for examination. Please check wait times at the top of the' +
              ' screen.',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 3',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'The \u003cb\u003eCOOP, L.L.C.\u003c/b\u003e designation(s) cannot be used with selected entity' +
          '  type of Corporation\u003c/b\u003e.',
          'designations': [
            'INCORPORATED',
            'CORPORATION',
            'LIMITED',
            'CORP.',
            'INC.',
            'LTD.',
            'INCORPOREE',
            'LIMITEE',
            'LTEE'
          ],
          'issue_type': 'designation_mismatch',
          'show_next_button': false,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'replace_designation',
              'header': 'Option 1',
              'line1': 'Change the designation from to one of the following:',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'change_entity_type',
              'header': 'Option 2',
              'line1': 'The designation you have selected is not appropriate for this entity type. You can choose to' +
              ' select a different type by pressing the \u0027RESTART and CHANGE TYPE\u0027 button.',
              'line2': '',
              'label': 'Change $entity_type to \u003cb\u003eINCORPORATED, CORPORATION, LIMITED, CORP., INC., LTD.,' +
              ' INCORPOREE, LIMITEE, LTEE\u003c/b\u003e'
            }
          ],
          'name_actions': [
            {
              'type': 'highlight',
              'word': 'L.L.C.',
              'index': 10
            }
          ]
        }
      ]
    }
  },
  {
    'test': 6,
    'name': 'ABC LTD PLUMBING',
    'corrected': 'ABC PLUMBING INCORPORATED',
    'analysisJSON': {
      'header': 'Further Action Required',
      'status': 'fa',
      'issues': [
        {
          'line1': 'Too similar to an existing name in queue.',
          'issue_type': 'queue_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING',
              'date': '2020-10-14',
              'start_date': '2020-07-14T23:38:10+00:00',
              'id': 'NR 9110602',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 2',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'Too similar to an existing name.',
          'issue_type': 'corp_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INCORPORATED',
              'date': '2020-10-14',
              'start_date': '2020-10-02T01:36:35.997287+00:00',
              'id': 'NR 9541590',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'send_to_examiner',
              'header': 'Option 2',
              'line1': 'You can choose to submit this name for examination. Please check wait times at the top of the' +
              ' screen.',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 3',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'The \u003cb\u003eLTD\u003c/b\u003e designation(s) cannot be used with selected entity type of' +
          ' Corporation\u003c/b\u003e.',
          'designations': [
            'INCORPORATED',
            'CORPORATION',
            'LIMITED',
            'CORP.',
            'INC.',
            'LTD.',
            'INCORPOREE',
            'LIMITEE',
            'LTEE'
          ],
          'issue_type': 'designation_mismatch',
          'show_next_button': false,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'replace_designation',
              'header': 'Option 1',
              'line1': 'Change the designation from to one of the following:',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'change_entity_type',
              'header': 'Option 2',
              'line1': 'The designation you have selected is not appropriate for this entity type. You can choose to' +
              ' select a different type by pressing the \u0027RESTART and CHANGE TYPE\u0027 button.',
              'line2': '',
              'label': 'Change $entity_type to \u003cb\u003eINCORPORATED, CORPORATION, LIMITED, CORP., INC., LTD.,' +
              ' INCORPOREE, LIMITEE, LTEE\u003c/b\u003e'
            }
          ],
          'name_actions': [
            {
              'type': 'highlight',
              'word': 'LTD',
              'index': 4
            }
          ]
        }
      ]
    }
  },
  {
    'test': 7,
    'name': 'ABC PLUMBING COOP',
    'corrected': 'ABC PLUMBING INCORPORATED',
    'analysisJSON': {
      'header': 'Further Action Required',
      'status': 'fa',
      'issues': [
        {
          'line1': 'Too similar to an existing name in queue.',
          'issue_type': 'queue_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING',
              'date': '2020-10-14',
              'start_date': '2020-07-14T23:38:10+00:00',
              'id': 'NR 9110602',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 2',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'Too similar to an existing name.',
          'issue_type': 'corp_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INCORPORATED',
              'date': '2020-10-14',
              'start_date': '2020-10-02T01:36:35.997287+00:00',
              'id': 'NR 9541590',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'send_to_examiner',
              'header': 'Option 2',
              'line1': 'You can choose to submit this name for examination. Please check wait times at the top of the' +
              ' screen.',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 3',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'The \u003cb\u003eCOOP\u003c/b\u003e designation(s) cannot be used with selected entity type of' +
          ' Corporation\u003c/b\u003e.',
          'designations': [
            'INCORPORATED',
            'CORPORATION',
            'LIMITED',
            'CORP.',
            'INC.',
            'LTD.',
            'INCORPOREE',
            'LIMITEE',
            'LTEE'
          ],
          'issue_type': 'designation_mismatch',
          'show_next_button': false,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'replace_designation',
              'header': 'Option 1',
              'line1': 'Change the designation from to one of the following:',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'change_entity_type',
              'header': 'Option 2',
              'line1': 'The designation you have selected is not appropriate for this entity type. You can choose to' +
              ' select a different type by pressing the \u0027RESTART and CHANGE TYPE\u0027 button.',
              'line2': '',
              'label': 'Change $entity_type to \u003cb\u003eINCORPORATED, CORPORATION, LIMITED, CORP., INC., LTD.,' +
              ' INCORPOREE, LIMITEE, LTEE\u003c/b\u003e'
            }
          ],
          'name_actions': [
            {
              'type': 'highlight',
              'word': 'COOP',
              'index': 5
            }
          ]
        }
      ]
    }
  },
  {
    'test': 8,
    'name': 'ABC PLUMBING LTD. INC.',
    'corrected': 'ABC PLUMBING LTD.',
    'analysisJSON': {
      'header': 'Further Action Required',
      'status': 'fa',
      'issues': [
        {
          'line1': 'Too similar to an existing name in queue.',
          'issue_type': 'queue_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING',
              'date': '2020-10-14',
              'start_date': '2020-07-14T23:38:10+00:00',
              'id': 'NR 9110602',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 2',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'Too similar to an existing name.',
          'issue_type': 'corp_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INCORPORATED',
              'date': '2020-10-14',
              'start_date': '2020-10-02T01:36:35.997287+00:00',
              'id': 'NR 9541590',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'send_to_examiner',
              'header': 'Option 2',
              'line1': 'You can choose to submit this name for examination. Please check wait times at the top of the' +
              ' screen.',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 3',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'There can be only one designation. You must choose either \u003cb\u003eLTD.\u003c/b\u003e  or' +
          '  \u003cb\u003eINC.\u003c/b\u003e',
          'designations': [
            'LTD.',
            'INC.'
          ],
          'issue_type': 'end_designation_more_than_once',
          'show_next_button': false,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'two_designations',
              'header': 'Option 1',
              'line1': 'Please select one of the designations listed here:',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': [
            {
              'type': 'highlight',
              'word': 'LTD.',
              'index': 6
            },
            {
              'type': 'highlight',
              'word': 'INC.',
              'index': 7
            }
          ]
        }
      ]
    }
  },
  {
    'test': 9,
    'name': 'ABC PLUMBING INC. LTD. LIMITED',
    'corrected': 'ABC PLUMBING INC.',
    'analysisJSON': {
      'header': 'Further Action Required',
      'status': 'fa',
      'issues': [
        {
          'line1': 'Too similar to an existing name in queue.',
          'issue_type': 'queue_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING',
              'date': '2020-10-14',
              'start_date': '2020-07-14T23:38:10+00:00',
              'id': 'NR 9110602',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 2',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'Too similar to an existing name.',
          'issue_type': 'corp_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INCORPORATED',
              'date': '2020-10-14',
              'start_date': '2020-10-02T01:36:35.997287+00:00',
              'id': 'NR 9541590',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'send_to_examiner',
              'header': 'Option 2',
              'line1': 'You can choose to submit this name for examination. Please check wait times at the top of the' +
              ' screen.',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 3',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'There can be only one designation. You must choose either \u003cb\u003eINC.\u003c/b\u003e  or' +
          '  \u003cb\u003eLTD.\u003c/b\u003e  or  \u003cb\u003eLIMITED\u003c/b\u003e',
          'designations': [
            'INC.',
            'LTD.',
            'LIMITED'
          ],
          'issue_type': 'end_designation_more_than_once',
          'show_next_button': false,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'two_designations',
              'header': 'Option 1',
              'line1': 'Please select one of the designations listed here:',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': [
            {
              'type': 'highlight',
              'word': 'INC.',
              'index': 7
            },
            {
              'type': 'highlight',
              'word': 'LTD.',
              'index': 8
            },
            {
              'type': 'highlight',
              'word': 'LIMITED',
              'index': 9
            }
          ]
        }
      ]
    }
  },
  {
    'test': 10,
    'name': 'ABC INC. PLUMBING LTD.',
    'corrected': 'ABC PLUMBING INC.',
    'analysisJSON': {
      'header': 'Further Action Required',
      'status': 'fa',
      'issues': [
        {
          'line1': 'Too similar to an existing name in queue.',
          'issue_type': 'queue_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING',
              'date': '2020-10-14',
              'start_date': '2020-07-14T23:38:10+00:00',
              'id': 'NR 9110602',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 2',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'Too similar to an existing name.',
          'issue_type': 'corp_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INCORPORATED',
              'date': '2020-10-14',
              'start_date': '2020-10-02T01:36:35.997287+00:00',
              'id': 'NR 9541590',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'send_to_examiner',
              'header': 'Option 2',
              'line1': 'You can choose to submit this name for examination. Please check wait times at the top of the' +
              ' screen.',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 3',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'There can be only one designation. You must choose either \u003cb\u003eINC.\u003c/b\u003e  or' +
          '  \u003cb\u003eLTD.\u003c/b\u003e',
          'designations': [
            'INC.',
            'LTD.'
          ],
          'issue_type': 'end_designation_more_than_once',
          'show_next_button': false,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'two_designations',
              'header': 'Option 1',
              'line1': 'Please select one of the designations listed here:',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': [
            {
              'type': 'highlight',
              'word': 'INC.',
              'index': 5
            },
            {
              'type': 'highlight',
              'word': 'LTD.',
              'index': 7
            }
          ]
        }
      ]
    }
  },
  {
    'test': 11,
    'name': 'INC. TRENT ACCOUNTING SERVICES',
    'corrected': 'TRENT ACCOUNTING SERVICES INC.',
    'analysisJSON': {
      'header': 'Further Action Required',
      'status': 'fa',
      'issues': [
        {
          'line1': 'The \u003cb\u003eINC.\u003c/b\u003e designation(s) must be at the end of the name.',
          'issue_type': 'designation_misplaced',
          'show_next_button': false,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'change designation at the end',
              'header': 'Option 1',
              'line1': 'Change designation order to the end of the name.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': [
            {
              'type': 'highlight',
              'word': 'INC.',
              'index': 4
            }
          ]
        }
      ]
    }
  },
  {
    'test': 12,
    'name': 'TRENT INC. ACCOUNTING SERVICES',
    'corrected': 'TRENT ACCOUNTING SERVICES INC.',
    'analysisJSON': {
      'header': 'Further Action Required',
      'status': 'fa',
      'issues': [
        {
          'line1': 'The \u003cb\u003eINC.\u003c/b\u003e designation(s) must be at the end of the name.',
          'issue_type': 'designation_misplaced',
          'show_next_button': false,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'change designation at the end',
              'header': 'Option 1',
              'line1': 'Change designation order to the end of the name.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': [
            {
              'type': 'highlight',
              'word': 'INC.',
              'index': 5
            }
          ]
        }
      ]
    }
  },
  {
    'test': 13,
    'name': 'ABC INC. L.L.C. PLUMBING',
    'corrected': 'ABC PLUMBING INCORPORATED',
    'analysisJSON': {
      'header': 'Further Action Required',
      'status': 'fa',
      'issues': [
        {
          'line1': 'Too similar to an existing name in queue.',
          'issue_type': 'queue_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INC.',
              'date': '2020-10-14',
              'start_date': '2020-07-21T19:57:00+00:00',
              'id': 'NR 8479118',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 2',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'Too similar to an existing name.',
          'issue_type': 'corp_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'ABC PLUMBING INCORPORATED',
              'date': '2020-10-14',
              'start_date': '2020-10-02T01:36:35.997287+00:00',
              'id': 'NR 9541590',
              'source': 'nr'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'send_to_examiner',
              'header': 'Option 2',
              'line1': 'You can choose to submit this name for examination. Please check wait times at the top of the' +
              ' screen.',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 3',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'The \u003cb\u003eINC.\u003c/b\u003e designation(s) must be at the end of the name.',
          'issue_type': 'designation_misplaced',
          'show_next_button': true,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'change designation at the end',
              'header': 'Option 1',
              'line1': 'Change designation order to the end of the name.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': [
            {
              'type': 'highlight',
              'word': 'INC.',
              'index': 5
            }
          ]
        },
        {
          'line1': 'The \u003cb\u003eL.L.C.\u003c/b\u003e designation(s) cannot be used with selected entity type of' +
          ' Corporation\u003c/b\u003e.',
          'designations': [
            'INCORPORATED',
            'CORPORATION',
            'LIMITED',
            'CORP.',
            'INC.',
            'LTD.',
            'INCORPOREE',
            'LIMITEE',
            'LTEE'
          ],
          'issue_type': 'designation_mismatch',
          'show_next_button': false,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'replace_designation',
              'header': 'Option 1',
              'line1': 'Change the designation from to one of the following:',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'change_entity_type',
              'header': 'Option 2',
              'line1': 'The designation you have selected is not appropriate for this entity type. You can choose to' +
              ' select a different type by pressing the \u0027RESTART and CHANGE TYPE\u0027 button.',
              'line2': '',
              'label': 'Change $entity_type to \u003cb\u003eINCORPORATED, CORPORATION, LIMITED, CORP., INC., LTD.,' +
              ' INCORPOREE, LIMITEE, LTEE\u003c/b\u003e'
            }
          ],
          'name_actions': [
            {
              'type': 'highlight',
              'word': 'L.L.C.',
              'index': 6
            }
          ]
        }
      ]
    }
  },
  {
    'test': 14,
    'name': 'INC. IDEAL L.L.C. ACCOUNTING SERVICES COMPANY LTD.',
    'corrected': 'IDEAL ACCOUNTING SERVICES COMPANY INCORPORATED',
    'analysisJSON': {
      'header': 'Further Action Required',
      'status': 'fa',
      'issues': [
        {
          'line1': 'Too similar to an existing name.',
          'issue_type': 'corp_conflict',
          'show_next_button': true,
          'show_examination_button': false,
          'conflicts': [
            {
              'name': 'IDEAL ACCOUNTING SERVICES LTD.',
              'date': '2020-10-15',
              'start_date': '2004-03-27T04:36:00+00:00',
              'id': '0331360',
              'source': 'corp'
            }
          ],
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'resolve_conflict',
              'header': 'Option 1',
              'line1': 'Add a word to the beginning of the name that sets it apart like a person’s name or initials.',
              'line2': 'Or remove the word(s) \u003cb\u003e\u003c/b\u003e and replace them with different ones.',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'send_to_examiner',
              'header': 'Option 2',
              'line1': 'You can choose to submit this name for examination. Please check wait times at the top of' +
              ' the screen.',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'conflict_self_consent',
              'header': 'Option 3',
              'line1': 'This name can be approved if you are the registered owner of the conflicting name, but you' +
              ' are required to send written consent to the BC Business Registry.',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': []
        },
        {
          'line1': 'There can be only one designation. You must choose either \u003cb\u003eINC.\u003c/b\u003e  or' +
          ' \u003cb\u003eLTD.\u003c/b\u003e',
          'designations': [
            'INC.',
            'LTD.'
          ],
          'issue_type': 'end_designation_more_than_once',
          'show_next_button': true,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'two_designations',
              'header': 'Option 1',
              'line1': 'Please select one of the designations listed here:',
              'line2': '',
              'label': ''
            }
          ],
          'name_actions': [
            {
              'type': 'highlight',
              'word': 'INC.',
              'index': 7
            },
            {
              'type': 'highlight',
              'word': 'LTD.',
              'index': 13
            }
          ]
        },
        {
          'line1': 'The \u003cb\u003eL.L.C.\u003c/b\u003e designation(s) cannot be used with selected entity type of' +
          ' Corporation\u003c/b\u003e.',
          'designations': [
            'INCORPORATED',
            'CORPORATION',
            'LIMITED',
            'CORP.',
            'INC.',
            'LTD.',
            'INCORPOREE',
            'LIMITEE',
            'LTEE'
          ],
          'issue_type': 'designation_mismatch',
          'show_next_button': false,
          'show_reserve_button': false,
          'show_examination_button': false,
          'setup': [
            {
              'button': '',
              'checkbox': '',
              'type': 'replace_designation',
              'header': 'Option 1',
              'line1': 'Change the designation from to one of the following:',
              'line2': '',
              'label': ''
            },
            {
              'button': '',
              'checkbox': '',
              'type': 'change_entity_type',
              'header': 'Option 2',
              'line1': 'The designation you have selected is not appropriate for this entity type. You can choose to' +
              ' select a different type by pressing the \u0027RESTART and CHANGE TYPE\u0027 button.',
              'line2': '',
              'label': 'Change $entity_type to \u003cb\u003eINCORPORATED, CORPORATION, LIMITED, CORP., INC., LTD.,' +
              ' INCORPOREE, LIMITEE, LTEE\u003c/b\u003e'
            }
          ],
          'name_actions': [
            {
              'type': 'highlight',
              'word': 'L.L.C.',
              'index': 9
            }
          ]
        }
      ]
    }
  }
]

export default testData
