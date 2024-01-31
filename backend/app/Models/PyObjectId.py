from bson import ObjectId

# Custom class for handling Pydantic validation of MongoDB ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        # Validate if the provided value is a valid ObjectId
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        # Modify Pydantic schema to represent the ObjectId as a string
        field_schema.update(type="string")
