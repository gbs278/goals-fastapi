import os
from Models.UserModels import UserModel, UpdateUserModel
from Models.GoalModels import GoalModel, UpdateGoalModel
from Models.StepModels import StepModel, UpdateStepModel
from dotenv import load_dotenv
from fastapi import FastAPI, Body, HTTPException, status, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from datetime import date
import datetime
from typing import Optional, List
import motor.motor_asyncio
load_dotenv()
# imports for passwords
from passlib.context import CryptContext
from Models.LoginModel import Login
from oauth import get_current_user
from jwttoken import create_access_token
from hashing import Hash
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
# end imports for password
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]
# end import for password
from fastapi import APIRouter
app = FastAPI()
# more login stuff 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# end more login stuff
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
users = client.users
goals = client.goals
steps = client.steps

### START OF PASSWORD HASHING STUFF ###

@app.post('/login')
async def login(request:OAuth2PasswordRequestForm = Depends()):
    #return request
    user = await users["users"].find_one({"name":request.username})
    #return jsonable_encoder(user)
    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not Hash.verify(user["password"],request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token = create_access_token(data={"sub": user["name"] })
    return {"access_token": str(user["_id"]), "token_type": "bearer"}

### END OF PASSWORD HASHING STUFF ###
### START OF USER ROUTES ###
@app.post("/api/create-user/{id}", response_description="Add new user" , response_model=UserModel) # 
async def create_user(request: UserModel):
    print(request)
    print(type(await users["users"].find_one({"name":request.name})), "length of user")
    if(user :=  await users["users"].find_one({"name":request.name})):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    hashed_pass = Hash.bcrypt(request.password)
    user_object = dict(request)
    user_object["password"] = hashed_pass
    user_to_return = await users["users"].insert_one(user_object)
    # return user as UserModel
    #user_to_return = await users["users"].find_one({"_id":user_id}) 
    return user_object
    
    
   

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
    if (user := await users["users"].find_one({"_id": ObjectId(id)})) is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User {id} not found")


@app.put("/api/update-user/{id}", response_description="Update a user", response_model=UserModel)
async def update_user(id: str, user: UpdateUserModel = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    hashed_pass = Hash.bcrypt(user["password"])
    user = dict(user)
    user["password"] = hashed_pass
    if len(user) >= 1:
        update_result = await users["users"].update_one({"_id": ObjectId(id)}, {"$set": user})
        if update_result.modified_count == 1:
            if (
                updated_user := await users["users"].find_one({"_id": ObjectId(id)})
            ) is not None:
                return updated_user

    if (existing_user := await users["users"].find_one({"_id": ObjectId(id)})) is not None:
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
    if (user := await users["users"].find_one({"_id": ObjectId(user_id)})) is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
   
    
    goal = jsonable_encoder(goal)
    new_goal = await goals["goals"].insert_one(goal)
    created_goals = await goals["goals"].find_one({"_id": new_goal.inserted_id})
    
    if new_goal.inserted_id is not None:
         associated_user =  await users["users"].update_one({"_id": ObjectId(user_id)}, {"$push": {'goals': new_goal.inserted_id}})

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


@app.get( "/api/get-goals", response_description="Get a single user's goals", )
async def show_goals_by_user(id: str):
    if (user := await users["users"].find_one({"_id": ObjectId(id)})) is not None:
        total_goals = []
        for(goal_id) in user["goals"]:
            if (goal := await goals["goals"].find_one({"_id": goal_id})) is not None:
                total_goals.append(goal)
        return total_goals

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@app.put("/api/update-goal/{goal_id}", response_description="Update a Goal by its ID", response_model=GoalModel)
async def update_goal(goal_id: str, goal: UpdateGoalModel = Body(...)):
    
    goal = {k: v for k, v in goal.dict().items() if v is not None}
    goal["end_date"] = datetime.datetime.combine(goal["end_date"], datetime.time())
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
    deleted_steps = await steps["steps"].delete_many({"goal_id": id})
    if delete_result.deleted_count == 1:
        return {"Message": "Goal deleted"}

    raise HTTPException(status_code=404, detail=f"Goal {id} not found")
### END OF GOAL ROUTES ###


### START OF STEP ROUTES ### 
@app.post("/api/create-step/{goal_id}", response_description="Add new step towards goals", response_model=StepModel) 
async def create_step(goal_id: str, step: StepModel = Body(...)):
    if (goal := await goals["goals"].find_one({"_id": goal_id})) is None:
        raise HTTPException(status_code=404, detail=f"Goal {goal_id} not found")
   
    
    step = jsonable_encoder(step)
    new_step = await steps["steps"].insert_one(step)
    created_steps = await steps["steps"].find_one({"_id": new_step.inserted_id})
    
    if new_step.inserted_id is not None:
         associated_goal =  await goals["goals"].update_one({"_id": goal_id}, {"$push": {'steps': new_step.inserted_id}})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_steps)


@app.get(
    "/api/get-all-steps", response_description="List all steps", response_model=List[StepModel]
)
async def list_steps():
    all_steps = await steps["steps"].find().to_list(1000)
    return all_steps

@app.get(
    "/api/get-step-by-step-id/{step_id}", response_description="Get a single step by Steps's ID", response_model=StepModel
)
async def show_step(id: str):
    if (step := await steps["steps"].find_one({"_id": id})) is not None:
        return step

    raise HTTPException(status_code=404, detail=f"Step {id} not found")


@app.get( "/api/get-steps/{goal_id}", response_description="Get a single goals's steps", )
async def show_steps_by_goal(id: str):
    if (goal := await goals["goals"].find_one({"_id": id})) is not None:
        total_steps = []
        for(step_id) in goal["steps"]:
            if (step := await steps["steps"].find_one({"_id": step_id})) is not None:
                total_steps.append(step)
        return total_steps

    raise HTTPException(status_code=404, detail=f"Goal {id} not found")


@app.put("/api/update-step/{step_id}", response_description="Update a Step by its ID", response_model=StepModel)
async def update_step(step_id: str, step: UpdateStepModel = Body(...)):
    
    step = {k: v for k, v in step.dict().items() if v is not None}
    if len(step) >= 1:
        update_result = await steps["steps"].update_one({"_id": step_id}, {"$set": step})
        if update_result.modified_count == 1:
            if (
                updated_step := await steps["steps"].find_one({"_id": step_id})
            ) is not None:
                return updated_step

    if (existing_step := await steps["steps"].find_one({"_id": step_id})) is not None:
        return existing_step

    raise HTTPException(status_code=404, detail=f"Step {step_id} not found")


@app.delete("/api/delete-step/{step_id}", response_description="Delete a step by Step ID")
async def delete_step(id: str):
    found_step = await steps["steps"].find_one({"_id": id})
    if found_step is None:
        raise HTTPException(status_code=404, detail=f"Step {id} not found")
    goal_id = found_step["goal_id"]
    found_goal = await goals["goals"].find_one({"_id": goal_id})
    goal_steps = found_goal["steps"]
    
    goal_steps.remove(id)


    
    delete_result = await steps["steps"].delete_one({"_id": id})
    deleted_goal_from_user = await goals["goals"].update_one({"_id": goal_id}, {"$set": {"steps" : goal_steps}})
    if delete_result.deleted_count == 1:
        return {"Message": "Step deleted"}

    raise HTTPException(status_code=404, detail=f"Step {id} not found")

### END OF STEP ROUTES ###