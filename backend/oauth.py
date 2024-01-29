# Importing necessary modules and packages
from fastapi import Depends, HTTPException
from jwttoken import verify_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Body, HTTPException, status, Request

# OAuth2PasswordBearer instance for token handling during authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to get the current user using OAuth2 token dependency
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Exception to handle failed token validation
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Verify the provided token and return the user if valid
    return verify_token(token, credentials_exception)
