import os
from .Models.UserModels import UserModel, UpdateUserModel
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
from jwttoken import create_access_token
from backend.app.hashing import Hash
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

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}



# Define an endpoint for user login using OAuth2 password flow
@app.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends()):
    # Retrieve user information from the database based on the provided username
    user = await users["users"].find_one({"name": request.username})
    # If the user is not found, raise an HTTP 404 NOT FOUND exception
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # Verify the provided password using the Hash class
    if not Hash.verify(user["password"], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # If username and password are valid, create an access token for the user
    access_token = create_access_token(data={"sub": user["name"]})
    # Return the access token along with token type as a response
    return {"access_token": str(user["_id"]), "token_type": "bearer"}


### START OF USER ROUTES ###

# Endpoint to create a new user with the provided user data
@app.post("/api/create-user", response_description="Add new user", response_model=UserModel)
async def create_user(request: UserModel):
    # Check if a user with the same name already exists
    if (user := await users["users"].find_one({"name": request.name})):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    # Hash the password before storing it in the database
    hashed_pass = Hash.bcrypt(request.password)
    
    # Convert the request object to a dictionary and replace the password with the hashed password
    user_object = dict(request)
    user_object["password"] = hashed_pass
    
    # Insert the user object into the database
    user_to_return = await users["users"].insert_one(user_object)
    
    # Return the created user as a UserModel
    return user_object

# Endpoint to retrieve a list of all users
@app.get(
    "/api/get-all-users", response_description="List all users", response_model=List[UserModel]
)
async def list_users():
    # Retrieve all users from the database and return the list
    all_users = await users["users"].find().to_list(1000)
    return all_users

# Endpoint to retrieve a single user based on the provided user ID
@app.get(
    "/api/get-user/{id}", response_description="Get a single user", response_model=UserModel
)
async def show_user(id: str):
    # Attempt to find and return the user with the given ID
    if (user := await users["users"].find_one({"_id": ObjectId(id)})) is not None:
        return user
    
    # If the user is not found, raise an HTTP 404 NOT FOUND exception
    raise HTTPException(status_code=404, detail=f"User {id} not found")



# Endpoint to update a user with the provided user ID and user data
@app.put("/api/update-user/{id}", response_description="Update a user", response_model=UserModel)
async def update_user(id: str, user: UpdateUserModel = Body(...)):
    # Extract non-null values from the user model
    user = {k: v for k, v in user.dict().items() if v is not None}
    
    # Hash the password before updating the user
    hashed_pass = Hash.bcrypt(user["password"])
    
    # Convert the user object to a dictionary and replace the password with the hashed password
    user = dict(user)
    user["password"] = hashed_pass
    
    # Check if there are any fields to update
    if len(user) >= 1:
        # Update the user in the database
        update_result = await users["users"].update_one({"_id": ObjectId(id)}, {"$set": user})
        
        # Check if the update was successful
        if update_result.modified_count == 1:
            # Retrieve and return the updated user
            if (updated_user := await users["users"].find_one({"_id": ObjectId(id)})) is not None:
                return updated_user

    # If the user does not exist, raise an HTTP 404 NOT FOUND exception
    if (existing_user := await users["users"].find_one({"_id": ObjectId(id)})) is not None:
        return existing_user
    raise HTTPException(status_code=404, detail=f"User {id} not found")

# Endpoint to delete a user with the provided user ID
@app.delete("/api/delete-user/{id}", response_description="Delete a user")
async def delete_user(id: str):
    # Attempt to delete the user from the database
    delete_result = await users["users"].delete_one({"_id": id})

    # Check if the user was successfully deleted
    if delete_result.deleted_count == 1:
        return {"message": f"User {id} deleted"}

    # If the user is not found, raise an HTTP 404 NOT FOUND exception
    raise HTTPException(status_code=404, detail=f"User {id} not found")

### END OF USER ROUTES ###


### START OF GOAL ROUTES ###
# Endpoint to create a new goal for a user with the provided user ID and goal data
@app.post("/api/create-goal/{id}", response_description="Add new goal", response_model=GoalModel) 
async def create_goal(user_id: str, goal: GoalModel = Body(...)):
    print(user_id)
    
    # Check if the user exists
    if (user := await users["users"].find_one({"_id": ObjectId(user_id)})) is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    # Convert the goal data to a JSON-compatible format
    goal = jsonable_encoder(goal)
    
    # Parse the end date string to a datetime object
    goal["end_date"] = datetime.datetime.strptime(goal["end_date"], "%Y-%m-%d")
    
    # Convert the goal data to a JSON-compatible format again
    goal = jsonable_encoder(goal)
    
    # Insert the new goal into the goals collection
    new_goal = await goals["goals"].insert_one(goal)
    
    # Retrieve the created goal from the goals collection
    created_goals = await goals["goals"].find_one({"_id": new_goal.inserted_id})
    
    # If the goal was successfully created, associate it with the user
    if new_goal.inserted_id is not None:
        associated_user =  await users["users"].update_one({"_id": ObjectId(user_id)}, {"$push": {'goals': new_goal.inserted_id}})
    
    # Return the created goal as a JSON response
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_goals)

# Endpoint to get a list of all goals
@app.get("/api/get-all-goals", response_description="List all goals", response_model=List[GoalModel])
async def list_goals():
    # Retrieve all goals from the goals collection and convert to a list
    all_goals = await goals["goals"].find().to_list(1000)
    return all_goals

# Endpoint to get a single goal by its ID
@app.get("/api/get-goal-by-goal-id/{goal_id}", response_description="Get a single goal by Goal's ID", response_model=GoalModel)
async def show_goal(id: str):
    # Retrieve the goal from the goals collection by its ID
    if (goal := await goals["goals"].find_one({"_id": id})) is not None:
        return goal
    
    # If the goal is not found, raise an HTTP 404 NOT FOUND exception
    raise HTTPException(status_code=404, detail=f"Goal {id} not found")

# Endpoint to get all goals associated with a user by user ID
@app.get("/api/get-goals", response_description="Get a single user's goals")
async def show_goals_by_user(id: str):
    # Check if the user exists
    if (user := await users["users"].find_one({"_id": ObjectId(id)})) is not None:
        total_goals = []
        # Iterate through the goal IDs associated with the user
        for(goal_id) in user["goals"]:
            # Retrieve each goal and append to the list
            if (goal := await goals["goals"].find_one({"_id": goal_id})) is not None:
                total_goals.append(goal)
        return total_goals
    
    # If the user is not found, raise an HTTP 404 NOT FOUND exception
    raise HTTPException(status_code=404, detail=f"User {id} not found")

# Endpoint to update a goal by its ID
@app.put("/api/update-goal/{goal_id}", response_description="Update a Goal by its ID", response_model=GoalModel)
async def update_goal(goal_id: str, goal: UpdateGoalModel = Body(...)):
    # Extract non-null values from the goal model
    goal = {k: v for k, v in goal.dict().items() if v is not None}
    
    # Combine the end date with a default time to create a datetime object
    goal["end_date"] = datetime.datetime.combine(goal["end_date"], datetime.time())
    
    # Check if there are any fields to update
    if len(goal) >= 1:
        # Update the goal in the goals collection
        update_result = await goals["goals"].update_one({"_id": goal_id}, {"$set": goal})
        
        # Check if the update was successful
        if update_result.modified_count == 1:
            # Retrieve and return the updated goal
            if (updated_goal := await goals["goals"].find_one({"_id": goal_id})) is not None:
                return updated_goal
    
    # If the goal is not found, raise an HTTP 404 NOT FOUND exception
    if (existing_goal := await goals["goals"].find_one({"_id": goal_id})) is not None:
        return existing_goal
    raise HTTPException(status_code=404, detail=f"Goal {goal_id} not found")

# Endpoint to increment the amount of completed steps for a goal
@app.put("/api/increment-completed-steps/{goal_id}", response_description="Increment the amount of steps completed by a goal")
async def increment_completed_steps(goal_id: str):
    # Find the goal by its ID
    found_goal = await goals["goals"].find_one({"_id": goal_id})
    
    # Get the current count of completed steps and increment by 1
    steps_done = found_goal["completed_steps"]
    steps_done += 1
    
    # Update the completed steps count in the goals collection
    update_result = await goals["goals"].update_one({"_id": goal_id}, {"$set": {"completed_steps": steps_done}})
    
    # If the goal is found, return the updated goal
    if (existing_goal := await goals["goals"].find_one({"_id": goal_id})) is not None:
        return existing_goal
    
    # If the goal is not found, raise an HTTP 404 NOT FOUND exception
    raise HTTPException(status_code=404, detail=f"Goal {goal_id} not found")

# Endpoint to decrement the amount of completed steps for a goal
@app.put("/api/decrement-completed-steps/{goal_id}", response_description="Decrement the amount of steps completed by a goal")
async def decrement_completed_steps(goal_id: str):
    # Find the goal by its ID
    found_goal = await goals["goals"].find_one({"_id": goal_id})
    
    # Get the current count of completed steps and decrement by 1
    steps_done = found_goal["completed_steps"]
    steps_done -= 1
    
    # Update the completed steps count in the goals collection
    update_result = await goals["goals"].update_one({"_id": goal_id}, {"$set": {"completed_steps": steps_done}})
    
    # If the goal is found, return the updated goal
    if (existing_goal := await goals["goals"].find_one({"_id": goal_id})) is not None:
        return existing_goal
    
    # If the goal is not found, raise an HTTP 404 NOT FOUND exception
    raise HTTPException(status_code=404, detail=f"Goal {goal_id} not found")

# Endpoint to delete a goal by its ID
@app.delete("/api/delete-goal/{goal_id}", response_description="Delete a goal by Goal ID")
async def delete_goal(id: str):
    # Find the goal by its ID
    found_goal = await goals["goals"].find_one({"_id": id})
    
    # Get the user ID associated with the goal
    user_id = found_goal["user_id"]
    
    # Find the user by their ID
    found_user = await users["users"].find_one({"_id": ObjectId(user_id)})
    
    # Get the list of goal IDs associated with the user
    user_goals = found_user["goals"]
    
    # Remove the goal ID from the user's goals list
    user_goals.remove(id)
    
    # Delete the goal from the goals collection
    delete_result = await goals["goals"].delete_one({"_id": id})
    
    # Update the user's goals list in the users collection
    deleted_goal_from_user = await users["users"].update_one({"_id": ObjectId(user_id)}, {"$set": {"goals": user_goals}})
    
    # Delete all steps associated with the goal
    deleted_steps = await steps["steps"].delete_many({"goal_id": id})
    
    # Check if the goal was successfully deleted
    if delete_result.deleted_count == 1:
        return {"Message": "Goal deleted"}
    
    # If the goal is not found, raise an HTTP 404 NOT FOUND exception
    raise HTTPException(status_code=404, detail=f"Goal {id} not found")

### END OF GOAL ROUTES ###


### START OF STEP ROUTES ### 
# Endpoint to create a new step for a goal with the provided goal ID and step data
@app.post("/api/create-step/{goal_id}", response_description="Add new step towards goals", response_model=StepModel) 
async def create_step(goal_id: str, step: StepModel = Body(...)):
    # Check if the goal exists
    if (goal := await goals["goals"].find_one({"_id": goal_id})) is None:
        raise HTTPException(status_code=404, detail=f"Goal {goal_id} not found")
    
    # Convert the step data to a JSON-compatible format
    step = jsonable_encoder(step)
    
    # Insert the new step into the steps collection
    new_step = await steps["steps"].insert_one(step)
    
    # Retrieve the created step from the steps collection
    created_steps = await steps["steps"].find_one({"_id": new_step.inserted_id})
    
    # If the step was successfully created, associate it with the goal
    if new_step.inserted_id is not None:
        associated_goal =  await goals["goals"].update_one({"_id": goal_id}, {"$push": {'steps': new_step.inserted_id}})
    
    # Return the created step as a JSON response
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_steps)

# Endpoint to get a list of all steps
@app.get("/api/get-all-steps", response_description="List all steps", response_model=List[StepModel])
async def list_steps():
    # Retrieve all steps from the steps collection and convert to a list
    all_steps = await steps["steps"].find().to_list(1000)
    return all_steps

# Endpoint to get a single step by its ID
@app.get("/api/get-step-by-step-id/{step_id}", response_description="Get a single step by Steps's ID", response_model=StepModel)
async def show_step(id: str):
    # Retrieve the step from the steps collection by its ID
    if (step := await steps["steps"].find_one({"_id": id})) is not None:
        return step
    
    # If the step is not found, raise an HTTP 404 NOT FOUND exception
    raise HTTPException(status_code=404, detail=f"Step {id} not found")

# Endpoint to get all steps associated with a goal by goal ID
@app.get("/api/get-steps/{goal_id}", response_description="Get a single goals's steps")
async def show_steps_by_goal(id: str):
    # Check if the goal exists
    if (goal := await goals["goals"].find_one({"_id": id})) is not None:
        total_steps = []
        # Iterate through the step IDs associated with the goal
        for(step_id) in goal["steps"]:
            # Retrieve each step and append to the list
            if (step := await steps["steps"].find_one({"_id": step_id})) is not None:
                total_steps.append(step)
        return total_steps
    
    # If the goal is not found, raise an HTTP 404 NOT FOUND exception
    raise HTTPException(status_code=404, detail=f"Goal {id} not found")

# Endpoint to update a step by its ID
@app.put("/api/update-step/{step_id}", response_description="Update a Step by its ID", response_model=StepModel)
async def update_step(step_id: str, step: UpdateStepModel = Body(...)):
    # Extract non-null values from the step model
    step = {k: v for k, v in step.dict().items() if v is not None}
    
    # Check if there are any fields to update
    if len(step) >= 1:
        # Update the step in the steps collection
        update_result = await steps["steps"].update_one({"_id": step_id}, {"$set": step})
        
        # Check if the update was successful
        if update_result.modified_count == 1:
            # Retrieve and return the updated step
            if (updated_step := await steps["steps"].find_one({"_id": step_id})) is not None:
                return updated_step
    
    # If the step is not found, raise an HTTP 404 NOT FOUND exception
    if (existing_step := await steps["steps"].find_one({"_id": step_id})) is not None:
        return existing_step
    raise HTTPException(status_code=404, detail=f"Step {step_id} not found")

# Endpoint to delete a step by its ID
@app.delete("/api/delete-step/{step_id}", response_description="Delete a step by Step ID")
async def delete_step(id: str):
    # Find the step by its ID
    found_step = await steps["steps"].find_one({"_id": id})
    
    # If the step is not found, raise an HTTP 404 NOT FOUND exception
    if found_step is None:
        raise HTTPException(status_code=404, detail=f"Step {id} not found")
    
    # Get the goal ID associated with the step
    goal_id = found_step["goal_id"]
    
    # Find the goal by its ID
    found_goal = await goals["goals"].find_one({"_id": goal_id})
    
    # Get the list of step IDs associated with the goal
    goal_steps = found_goal["steps"]
    
    # Remove the step ID from the goal's steps list
    goal_steps.remove(id)
    
    # Delete the step from the steps collection
    delete_result = await steps["steps"].delete_one({"_id": id})
    
    # Update the goal's steps list in the goals collection
    deleted_goal_from_user = await goals["goals"].update_one({"_id": goal_id}, {"$set": {"steps" : goal_steps}})
    
    # Check if the step was successfully deleted
    if delete_result.deleted_count == 1:
        return {"Message": "Step deleted"}
    
    # If the step is not found, raise an HTTP 404 NOT FOUND exception
    raise HTTPException(status_code=404, detail=f"Step {id} not found")


### END OF STEP ROUTES ###
