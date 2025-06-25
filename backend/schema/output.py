from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class InferenceOutput(BaseModel):
   user_id: int
   response: Optional[str]
   username: str
   timestamp: datetime

class UserHistory(BaseModel):
   user_id: int
   username: str
   chats: List[InferenceOutput]

class AccessToken(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" * 3)
    token_type: str = Field(..., example="bearer")

class UserInfo(BaseModel):
    joined: datetime = Field(..., example="2023-01-01T00:00:00")
    username: str = Field(..., example="shaun")
    email: str = Field(..., example="shaun@gmail.com")

class JsonResponse(BaseModel):
    message: str = Field(..., example="Operation successful")
