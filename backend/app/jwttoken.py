from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve secret key and algorithm from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define TokenData model representing the data stored in the access token
class TokenData(BaseModel):
    username: Optional[str] = None

# Function to create an access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Encode the JWT token using the provided data, secret key, and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify an access token
def verify_token(token: str, credentials_exception):
    try:
        # Decode the JWT token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Create a TokenData instance with the decoded username
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
