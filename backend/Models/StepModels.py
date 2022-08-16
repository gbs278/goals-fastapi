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
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    description: str = Field(...)
    goal_id: PyObjectId = Field(default_factory=PyObjectId, alias="goal_id")
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
    description: Optional[str]
    goal_id : Optional[PyObjectId]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "description": "Take Guitar Lesson",
                "goal_id" : "1234456789"
            }
        }
