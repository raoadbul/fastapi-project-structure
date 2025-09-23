import jwt
from datetime import datetime, timedelta
from typing import Any
import os
from typing import Any, Dict
from dotenv import load_dotenv
load_dotenv()

# Secret key to encode/decode JWT tokens
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))  # Token expiration time in minutes

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_user_token(token: str) -> Dict[str, Any]:
    try:
        # Decode the token and verify its validity
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check if the token is expired
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise jwt.ExpiredSignatureError("Token has expired")
        
        return payload  # This contains the user information (e.g., email or user ID)
    
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.PyJWTError as e:
        raise Exception(f"Invalid token: {str(e)}")