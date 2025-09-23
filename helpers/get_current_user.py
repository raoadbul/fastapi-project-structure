from fastapi import Depends, HTTPException, status
from models.user import User
from helpers.user_token import decode_user_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated

security = HTTPBearer()

async def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_user_token(token)
        user_id = payload["id"]
    except:
        raise credentials_exception
    
    if user_id is None:
        raise credentials_exception
    
    try:
        user = await User.get(id=user_id)
        return user
    except:
        raise credentials_exception
