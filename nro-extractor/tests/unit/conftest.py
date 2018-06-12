import json
import pytest
from flask import Flask, Blueprint
from flask.testing import FlaskClient
# import flask_restplus as restplus
from api import create_app, db
from config import TestConfig
import os
import logging


@pytest.fixture
def client():
    logging.log(logging.INFO, TestConfig().SQLALCHEMY_DATABASE_URI)

    app = create_app(TestConfig())
    client = app.test_client()

    yield client

