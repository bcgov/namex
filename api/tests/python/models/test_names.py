from namex.models import Name, NameSchema
import sys


def test_name_create(session):
    """Start with a blank database."""

    name = Name(name= "my good company", state= "NE", conflict1= None, conflict3= None, consumptionDate= None, conflict2= None, designation= None, conflict1_num= None, decision_text= None, conflict3_num= None, conflict2_num= None, choice= 1)

    session.add(name)
    session.commit()

    assert name.id is not None


def test_name_schema():
    """Start with a blank database."""
    name_json = {"name": "my good company", "state": "NE", "conflict1": "conflict1", "conflict2": "conflict2", "conflict3": "conflict3", "consumptionDate": None,  "designation": "LLC", "conflict1_num": "NR 0000001", "decision_text": "my descision", "conflict3_num": "NR 0000003", "conflict2_num": "NR 0000002", "choice": 1}

    name_schema = NameSchema()

    name = Name(name= "my good company", state= "NE", conflict1= "conflict1", conflict2= "conflict2", conflict3= "conflict3", consumptionDate= None,  designation= "LLC", conflict1_num= "NR 0000001", decision_text= "my descision", conflict3_num= "NR 0000003", conflict2_num= "NR 0000002", choice= 1)

    name_dump = name_schema.dump(name).data

    assert name_dump == name_json


def test_name_schema_db_update(session):
    """Start with a blank database."""

    # setup
    test_name = "my good company"
    name_json = {"name": "my good company", "state": "NE", "conflict1": "conflict1", "conflict2": "conflict2", "conflict3": "conflict3", "consumptionDate": None,  "designation": "LLC", "conflict1_num": "NR 0000001", "decision_text": "my descision", "conflict3_num": "NR 0000003", "conflict2_num": "NR 0000002", "choice": 1}
    name_schema = NameSchema()

    # create a name and add to the DB
    name = Name(name="temp")
    session.add(name)
    session.commit()

    # update the name and resave
    name_schema.load(name_json, instance=name, partial=False)
    session.add(name)
    session.commit()

    assert name.id is not None
    assert name.name == test_name
    assert name_json == name_schema.dump(name).data


def test_name_schema_db_query_update(session):
    """Start with a blank database."""

    # setup
    test_name = "my good company"
    name_json = {"name": test_name, "state": "NE", "conflict1": "conflict1", "conflict2": "conflict2", "conflict3": "conflict3", "consumptionDate": None,  "designation": "LLC", "conflict1_num": "NR 0000001", "decision_text": "my descision", "conflict3_num": "NR 0000003", "conflict2_num": "NR 0000002", "choice": 1}
    name_schema = NameSchema()

    # create a name
    name = Name(name="temp")
    session.add(name)
    session.commit()
    name_id = name.id

    # update it from the json data vi the schema loader
    name_schema.load(name_json, instance=name, partial=False)
    session.add(name)
    session.commit()

    # get the name from the data base & assert it was updated
    name = None
    name = Name.query.filter_by(name=test_name).one_or_none()
    assert name.id is not None
    assert name.id == name_id
    assert name.name == test_name
    assert name_json == name_schema.dump(name).data
