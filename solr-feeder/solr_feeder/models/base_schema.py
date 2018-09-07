
import marshmallow_sqlalchemy


# The abstract class that corresponds to a database schema.
class BaseSchema(marshmallow_sqlalchemy.ModelSchema):
    # If we get null values from the database, convert them from None to ''.
    #
    # Note this needs to be completed - not working.
    @classmethod
    def dump_clean(cls, result) -> dict:
        json = cls.dump(cls, result).data

        for key in json.keys():
            if not json[key]:
                json[key] = ''

        return json
