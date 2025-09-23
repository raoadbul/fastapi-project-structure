from fastapi import APIRouter

router = APIRouter()

@router.post('/register')
async def register():
    return "User Registered"

@router.post('/login')
async def login():
    return "User Logged In"