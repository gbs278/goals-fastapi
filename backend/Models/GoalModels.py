import os
from Models.PyObjectId import PyObjectId
from dotenv import load_dotenv
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from datetime import date, datetime
from typing import Optional, List
import motor.motor_asyncio
load_dotenv()


class GoalModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    description: str = Field(...)
    start_date: date=  date.today()
    end_date: datetime = Field(default_factory=datetime, alias="end_date")
    completed: bool = Field(default_factory=bool, alias="completed")
    user: PyObjectId = Field(default_factory=PyObjectId, alias="user_id")
    # @TO-DO need to add in all the steps, do this after the steps model has been created
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "description": "Learn Guitar",
                "user_id" : "1234456789",
                "end_date": "2020-01-31",
                "completed": False

            }
        }


class UpdateGoalModel(BaseModel):
    end_date: Optional[date] = Field(default_factory=date, alias="end_date")
    description: Optional[str]
    completed: Optional[bool]
    user_id : Optional[PyObjectId]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "end_date": "2020-01-31",
                "description": """Learn Guitar""",
                "completed": False,
                "user_id" : "1234456789"
            }
        }
