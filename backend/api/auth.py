import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Union, Any, List
from fastapi import APIRouter, HTTPException, Body, Depends, Response, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from models import User, OtpStore
from schema.input import OTPVerify, ResetPassword, UpdatePassword, Register
from schema.input import Password, Email
from schema.output import AccessToken, AccessToken, JsonResponse
from sqlalchemy.orm import Session
from api.utils import (
    create_access_token, 
    authenticate_user, 
    create_otp, 
    send_email_otp, 
    email_authentication,
    start_session,
    hash_password,
    get_current_user
)

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
router = APIRouter()

@router.post("/login", response_model=AccessToken)
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(start_session)
    ) -> AccessToken:
    user = authenticate_user(form_data.username, form_data.password, session)
    token = create_access_token(data={"sub": user.email})

    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        max_age= ACCESS_TOKEN_EXPIRE_MINUTES * 60,      
        expires= datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),   
        secure=True,          
        samesite="lax",      
    )
    return AccessToken(access_token=token, token_type="bearer")

@router.get("/logout")
def logout(user = Depends(get_current_user)):
    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie("access_token")
    return response

@router.post("/register", response_model=JsonResponse)
def register(
    register: Register,
    session: Session = Depends(start_session)
    ) -> JsonResponse:
    try:
        if session.query(User).filter(User.email==register.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email already registered"
                )
        account = User(
            username=register.username, 
            hashed_password=hash_password(register.password), 
            email=register.email
            )
        session.add(account)
        session.commit()
        session.refresh(account)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Database error: {str(e)}"
            )
    return JsonResponse(message="Account created successfully")

@router.put("/update_email", response_model=JsonResponse)
def update_email(
    email: Email = Body(...), 
    user: User = Depends(get_current_user),
    session: Session = Depends(start_session)
    ) -> JsonResponse:
    try:
        session.query(User).filter(
            User.id == user.id).update({"email": email.email}
            )
        session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Database error: {str(e)}"
            )
    return JsonResponse(message="Email updated successfully")

@router.put("/send_otp_to_email", response_model=JsonResponse)
def send_otp_to_email(
    email: Email = Body(...),
    session: Session = Depends(start_session)
    ) -> JsonResponse:
    user = email_authentication(email.email, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Email not found"
            )
    otp = create_otp(email.email, session)
    send_email_otp(email.email, otp)
    return JsonResponse(message=f"OTP sent successfully {otp}")


@router.post("/verify_otp", response_model=JsonResponse)
def verify_otp(
    data: OTPVerify = Body(...),
    session: Session = Depends(start_session)
    ) -> JsonResponse:
    otp_store = session.query(OtpStore).filter(
        OtpStore.email == data.email,
        OtpStore.otp == data.otp
        ).first()
    if not otp_store:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid OTP"
        )
    if datetime.now() > otp_store.expire_at:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="OTP expired"
        )
    otp_store.is_verified = True
    session.commit()
    return JsonResponse(message="OTP verified successfully")


@router.put("/reset_password", response_model=JsonResponse)
def reset_password(
    data: ResetPassword = Body(...),
    session: Session = Depends(start_session)
    ) -> JsonResponse:
    user = email_authentication(data.email, session)
    otp_record = session.query(OtpStore).filter(
        OtpStore.email == data.email,
        OtpStore.is_verified == True
        ).first()
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="OTP not verified"
        )
    user.hashed_password = hash_password(data.new_password)
    session.delete(otp_record)
    session.commit()
    return JsonResponse(message="Password reset successfully")