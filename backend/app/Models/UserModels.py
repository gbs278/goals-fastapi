from dotenv import load_dotenv
from pydantic import BaseModel, Field
from .PyObjectId import PyObjectId
from bson import ObjectId
from typing import Optional, List
load_dotenv()

class UserModel(BaseModel):
    # User's name
    name: str = Field(...)
    
    # User's password
    password: str = Field(...)
    
    # List of goal IDs associated with the user
    goals: List[PyObjectId] = Field(default_factory=list, alias="goals")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "password": "mypassword"
            }
        }

class UpdateUserModel(BaseModel):
    # Optional new name for updating the user
    name: Optional[str]
    
    # Optional new password for updating the user
    password: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "password": "MyNewPassword!"
            }
        }
