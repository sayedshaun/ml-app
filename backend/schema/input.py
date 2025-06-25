from pydantic import BaseModel, Field
from typing import Optional


class Login(BaseModel):
   email: str = Field(..., example="shaun@gmail.com")
   password: Optional[str] = Field(..., example="1234")

class Register(BaseModel): 
   email: str = Field(..., example="shaun@gmail.com")
   username: str = Field(..., example="shaun")
   password: Optional[str] = Field(..., example="1234")

class Inference(BaseModel):
   response: str = Field(..., example="This is a response")

class UserName(BaseModel):
   username: str = Field(..., example="shaun")

class Password(BaseModel):
   password: Optional[str] = Field(..., example="1234")

class Email(BaseModel):
   email: str = Field(..., example="shaun@gmail.com")

class UpdatePassword(BaseModel):
    old_password: str = Field(..., example="1234")
    new_password: str = Field(..., example="1234567")

class ResetPassword(BaseModel):
    email: str = Field(..., example="shaun@gmail.com")
    new_password: str = Field(..., example="1234567")

class OTPVerify(BaseModel):
    email: str = Field(..., example="shaun@gmail.com")
    otp: str = Field(..., example="123456")