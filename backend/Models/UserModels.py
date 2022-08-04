import os
from dotenv import load_dotenv
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from Models.PyObjectId import PyObjectId
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
load_dotenv()
from .GoalModels import GoalModel, UpdateGoalModel

class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    password: str = Field(...)
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
    name: Optional[str]
    course: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "password": "MyNewPassword!"
            }
        }
