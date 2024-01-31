import os
from dotenv import load_dotenv
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from .PyObjectId import PyObjectId
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio

load_dotenv()

# Define Login model for handling user login information
class Login(BaseModel):
    name: str = Field(...)  # User name for login
    password: str = Field(...)  # User password for login
