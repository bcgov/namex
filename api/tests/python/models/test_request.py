from flask import jsonify
from unittest import mock
import pytest


def test_get_queued_oldest(client, app):

    # SETUP #####
    # add NR to database
    from namex.models import Request as RequestDAO, State, User
    nr = RequestDAO()
    nr.nrNum='NR 0000001'
    nr.stateCd = State.DRAFT
    nr.save_to_db()

    user = User(username='testUser', firstname='first', lastname='last', sub='idir/funcmunk', iss='keycloak')
    user.save_to_db()

    nr_oldest, new_req = RequestDAO.get_queued_oldest(user)

    # Tests ####
    assert nr.nrNum == nr_oldest.nrNum


def test_get_queued_oldest_multirow(client, app):

    # add NR to database
    from namex.models import Request as RequestDAO, State, User
    nr_first = RequestDAO()
    nr_first.nrNum='NR 0000001'
    nr_first.stateCd = State.DRAFT
    nr_first.save_to_db()

    for i in range(2,12):
        nr = RequestDAO()
        nr.nrNum = 'NR {0:07d}'.format(i)
        nr.stateCd = State.DRAFT
        nr.save_to_db()

    user = User(username='testUser', firstname='first', lastname='last', sub='idir/funcmunk', iss='keycloak')
    user.save_to_db()

    nr_oldest, new_req = RequestDAO.get_queued_oldest(user)

    # Tests ####
    assert nr_first.nrNum == nr_oldest.nrNum


def test_get_queued_empty_queue(client, app):

    # SETUP #####
    # add NR to database
    from namex.models import Request as RequestDAO, User
    from namex.exceptions import BusinessException

    user = User(username='testUser', firstname='first', lastname='last', sub='idir/funcmunk', iss='keycloak')
    user.save_to_db()

    with pytest.raises(BusinessException) as e_info:
        nr_oldest, new_req = RequestDAO.get_queued_oldest(user)
