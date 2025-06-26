from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, Body, status
from api.utils import get_current_user, start_session
from models import User
from schema.input import UserName
from schema.output import UserHistory, InferenceOutput, UserInfo, JsonResponse
from models import Predictions
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/user_info")
def user_info(
    user: User = Depends(get_current_user),
    session: Session = Depends(start_session)
    ) -> UserInfo:
    return UserInfo(
        joined=user.create_time,
        username=user.username,
        email=user.email
    )

@router.get("/prediction_history", response_model=UserHistory)
def prediction_history(
    user: User = Depends(get_current_user),
    session: Session = Depends(start_session)
    ) -> UserHistory:
    return UserHistory(
        user_id=user.id,
        username=user.username,
        chats=[
            InferenceOutput(
                user_id=chat.user_id,
                response=chat.response,
                username=chat.sender,
                timestamp=chat.timestamp
            )
            for chat in user.predictions
        ]
    )
  
@router.put("/update_username", response_model=JsonResponse)
def update_username(
    username: UserName = Body(...), 
    user: User = Depends(get_current_user),
    session: Session = Depends(start_session)
    ) -> JsonResponse:
    exist_user = session.query(User).filter(
        User.username == username.username
        ).first()
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already exists"
            )
    session.query(User).filter(
        User.id == user.id).update({"username": username.username}
    )
    session.commit()
    return JsonResponse(message="Username updated successfully")



@router.delete("/delete_prediction/{id}", response_model=JsonResponse)
def delete_prediction(
    id: int, user: User = Depends(get_current_user),
    session: Session = Depends(start_session)
    ) -> JsonResponse:
    chat = session.query(Predictions).filter(
        Predictions.id == id, Predictions.user_id == user.id
        ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Chat not found"
            )
    session.delete(chat)
    session.commit()
    return JsonResponse(message="Chat deleted successfully")
        
   