import os
from Models.UserModels import UserModel, UpdateUserModel
from Models.GoalModels import GoalModel, UpdateGoalModel
from dotenv import load_dotenv
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from datetime import date
import datetime
from typing import Optional, List
import motor.motor_asyncio
load_dotenv()

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
users = client.users
goals = client.goals


### START OF USER ROUTES ###
@app.post("/api/create-user", response_description="Add new user", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await users["users"].insert_one(user)
    created_users = await users["users"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_users)


@app.get(
    "/api/get-all-users", response_description="List all users", response_model=List[UserModel]
)
async def list_users():
    all_users = await users["users"].find().to_list(1000)
    return all_users


@app.get(
    "/api/get-user/{id}", response_description="Get a single user", response_model=UserModel
)
async def show_user(id: str):
    if (user := await users["users"].find_one({"_id": id})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@app.put("/api/update-user/{id}", response_description="Update a user", response_model=UserModel)
async def update_user(id: str, user: UpdateUserModel = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}

    if len(user) >= 1:
        update_result = await users["users"].update_one({"_id": id}, {"$set": user})

        if update_result.modified_count == 1:
            if (
                updated_user := await users["users"].find_one({"_id": id})
            ) is not None:
                return updated_user

    if (existing_user := await users["users"].find_one({"_id": id})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@app.delete("/api/delete-user/{id}", response_description="Delete a user")
async def delete_user(id: str):
    delete_result = await users["users"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return {"message": f"User {id} deleted"}

    raise HTTPException(status_code=404, detail=f"User {id} not found")
### END OF USER ROUTES ###


### START OF GOAL ROUTES ###
@app.post("/api/create-goal/{id}", response_description="Add new goal", response_model=GoalModel) 
async def create_goal(user_id: str, goal: GoalModel = Body(...)):
    if (user := await users["users"].find_one({"_id": user_id})) is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
   
    
    goal = jsonable_encoder(goal)
    new_goal = await goals["goals"].insert_one(goal)
    created_goals = await goals["goals"].find_one({"_id": new_goal.inserted_id})
    
    if new_goal.inserted_id is not None:
         associated_user =  await users["users"].update_one({"_id": user_id}, {"$push": {'goals': new_goal.inserted_id}})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_goals)


@app.get(
    "/api/get-all-goals", response_description="List all goals", response_model=List[GoalModel]
)
async def list_goals():
    all_goals = await goals["goals"].find().to_list(1000)
    return all_goals


@app.get(
    "/api/get-goal-by-goal-id/{goal_id}", response_description="Get a single goal by Goal's ID", response_model=GoalModel
)
async def show_goal(id: str):
    if (goal := await goals["goals"].find_one({"_id": id})) is not None:
        return goal

    raise HTTPException(status_code=404, detail=f"Goal {id} not found")


@app.get( "/api/get-goals/{user_id}", response_description="Get a single user's goals", )
async def show_goals(id: str):
    if (user := await users["users"].find_one({"_id": id})) is not None:
        total_goals = []
        for(goal_id) in user["goals"]:
            if (goal := await goals["goals"].find_one({"_id": goal_id})) is not None:
                total_goals.append(goal)
        return total_goals

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@app.put("/api/update-goal/{goal_id}", response_description="Update a Goal by its ID", response_model=GoalModel)
async def update_goal(goal_id: str, goal: UpdateGoalModel = Body(...)):
    
    goal = {k: v for k, v in goal.dict().items() if v is not None}
    print(type(goal["end_date"]))
    goal["end_date"] = datetime.datetime.combine(goal["end_date"], datetime.time())
    print(goal["end_date"])
    if len(goal) >= 1:
        update_result = await goals["goals"].update_one({"_id": goal_id}, {"$set": goal})
        if update_result.modified_count == 1:
            if (
                updated_goal := await goals["goals"].find_one({"_id": goal_id})
            ) is not None:
                return updated_goal

    if (existing_goal := await goals["goals"].find_one({"_id": goal_id})) is not None:
        return existing_goal

    raise HTTPException(status_code=404, detail=f"Goal {goal_id} not found")


@app.delete("/api/delete-goal/{goal_id}", response_description="Delete a goal by Goal ID")
async def delete_goal(id: str):
    found_goal = await goals["goals"].find_one({"_id": id})
    user_id = found_goal["user_id"]
    found_user = await users["users"].find_one({"_id": user_id})
    user_goals = found_user["goals"]
    user_goals.remove(id)
    
    delete_result = await goals["goals"].delete_one({"_id": id})
    deleted_goal_from_user = await users["users"].update_one({"_id": user_id}, {"$set": {"goals" : user_goals}})
    if delete_result.deleted_count == 1:
        return {"Message": "Goal deleted"}

    raise HTTPException(status_code=404, detail=f"Goal {id} not found")
### END OF GOAL ROUTES ###