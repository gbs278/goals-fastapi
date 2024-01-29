import os
from Models.PyObjectId import PyObjectId
from .GoalModels import GoalModel, UpdateGoalModel
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

class StepModel(BaseModel):
    # Step ID with default factory to generate a new ObjectId
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    # Description of the step
    description: str = Field(...)
    
    # Goal ID associated with the step
    goal_id: PyObjectId = Field(default_factory=PyObjectId, alias="goal_id")
    
    # Boolean indicating whether the step is completed
    completed: bool = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "description": "Take Guitar Lesson",
                "goal_id" : "1234456789"
            }
        }

class UpdateStepModel(BaseModel):
    # Optional description for updating the step
    description: Optional[str]
    
    # Optional Goal ID for updating the associated goal
    goal_id : Optional[PyObjectId]
    
    # Boolean indicating whether the step is completed
    completed: bool = False

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "description": "Take Guitar Lesson",
                "goal_id" : "1234456789",
                "completed": "true"
            }
        }
