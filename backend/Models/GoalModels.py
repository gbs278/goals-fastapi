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

# Define GoalModel representing a goal in the application
class GoalModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    description: str = Field(...)  # Description of the goal
    start_date: date = date.today()  # Start date of the goal (defaults to the current date)
    end_date: str = Field(...)  # End date of the goal
    completed: bool = False  # Boolean indicating whether the goal is completed
    user: PyObjectId = Field(default_factory=PyObjectId, alias="user_id")  # User ID associated with the goal
    steps: List[PyObjectId] = Field(default_factory=list, alias="steps")  # List of step IDs associated with the goal
    completed_steps: int = 0  # Number of steps completed for the goal

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "description": "Learn Guitar",
                "user_id": "1234456789",
                "end_date": "2020-01-31"
            }
        }

# Define UpdateGoalModel representing the model used for updating a goal
class UpdateGoalModel(BaseModel):
    end_date: Optional[date] = Field(default_factory=date, alias="end_date")
    description: Optional[str]
    completed: Optional[bool]
    user_id: Optional[PyObjectId]
    completed_steps: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "end_date": "2020-01-31",
                "description": """Learn Guitar""",
                "completed": True,
                "user_id": "1234456789",
                "completed_steps": "5"
            }
        }
