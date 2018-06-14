from app import db


class Request(db.Model):
    # find out core fields and add them
    id = db.Column(db.Integer, primary_key=True)

    # intitialize self
    def __init__(self, *args, **kwargs):
        pass

    def json(self):

        return {'id': self.id}

    @classmethod
    def get_corp_details(cls, corp_id):
        """Gets the corporate details associated with the given ID
        """
        corp_details = corp_id  # access database with proper query -- how is it sent back?

        return corp_details
