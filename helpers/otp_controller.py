from models.user import User
from fastapi import APIRouter,  HTTPException
from pydantic import BaseModel
import pyotp
from datetime import datetime, timedelta

router = APIRouter()


class OTPRequest(BaseModel):
    email: str

class OTPVerify(BaseModel):
    email: str
    otp: str

@router.post("/generate-otp")
async def generate_otp(request: OTPRequest):
    # Fetch the user by email
    user = await User.filter(email=request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Check if OTP was recently generated (within the last 5 minutes)
    if user.otp_created_at:
        otp_created_at = datetime.strptime(user.otp_created_at, "%Y-%m-%d %H:%M:%S.%f")
        # Check if OTP was recently generated (within the last 5 minutes)
        if datetime.now() - otp_created_at < timedelta(minutes=5):
            raise HTTPException(status_code=400, detail="OTP already generated. Please wait before requesting again.")


    # Generate OTP and set it for the user
    # totp = pyotp.TOTP(pyotp.random_base32())
    # otp = totp.now()
    otp=123456
    user.otp = otp
    user.otp_created_at = datetime.now()
    await user.save()

    # In real applications, send the OTP via email/SMS instead of returning it
    return {"message": "OTP generated successfully.", "otp": otp}

@router.post("/verify-otp")
async def verify_otp(request: OTPVerify):
    # Fetch the user by email
    user = await User.filter(email=request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Check if OTP is valid
    if not user.otp or not user.otp_created_at:
        raise HTTPException(status_code=400, detail="No OTP generated for this user.")
    
    otp_created_at = datetime.strptime(user.otp_created_at, "%Y-%m-%d %H:%M:%S.%f")
    
    # Check if the OTP is expired (valid for 5 minutes)
    if datetime.now() - otp_created_at > timedelta(minutes=5):
        raise HTTPException(status_code=400, detail="OTP has expired. Please generate a new one.")

    # Verify the OTP
    if user.otp != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP.")

    # Mark user as verified and clear OTP fields
    user.is_verified = True
    user.otp = None
    user.otp_created_at = None
    await user.save()

    return {"message": "OTP verified successfully."}