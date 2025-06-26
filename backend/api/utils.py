import os
from datetime import datetime, timedelta
import random
from typing import Any, Dict, Union
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from schema.input import Email, Password
from models import User, OtpStore
from db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from passlib.context import CryptContext
from fastapi import Cookie, Header
from dotenv import load_dotenv

load_dotenv()
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def start_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(email: Email, password: Password, session: Session) -> User:
    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email not found"
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Password is incorrect"
        )
    return user

def email_authentication(email: Email, session: Session) -> User:
    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email not found",
        )
    return user
    
def get_current_user(
    access_token: str = Cookie(None),
    session: Session = Depends(start_session)
    ) -> User:
    raw_token = access_token
    if raw_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scheme, _, token = raw_token.partition(" ")
    if scheme.lower() != "bearer":
        token = raw_token

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise ValueError()
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired, please login again",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_otp(email: str, session: Session = Depends(start_session)) -> str:
    #otp = random.randint(10000, 99999)
    otp = 100000
    expire_at = datetime.now() + timedelta(minutes=2)
    session.query(OtpStore).filter(OtpStore.email == email).delete()
    session.add(OtpStore(email=email, otp=otp, expire_at=expire_at))
    session.commit()
    return str(otp)

def send_email_otp(email: str, otp: str):
    print(f"Send to {email}: Your OTP is {otp}")