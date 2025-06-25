import os 
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.utils import get_current_user, start_session
from models import User, Predictions
import requests
import json
from schema.ml import NERInput, NEROutput, QAInput, QAOutput, SentimentInput, SentimentOutput
from dotenv import load_dotenv

load_dotenv()
NER_ENDPOINT = os.getenv("NER_ENDPOINT")
QA_ENDPOINT = os.getenv("QA_ENDPOINT")
SENTIMENT_ENDPOINT = os.getenv("SENTIMENT_ENDPOINT")
router = APIRouter()

@router.post("/ner_prediction", response_model=NEROutput)
def ner_prediction(
    inputs: NERInput, 
    user: User = Depends(get_current_user),
    session: Session = Depends(start_session)
    ) -> Dict[str, str]:  
   try:
       response = requests.post(NER_ENDPOINT, json=inputs.model_dump())
       response.raise_for_status()
       data = response.json()
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
           detail=f"Prediction service error: {str(e)}"
       )
   try:
       db_chat = Predictions(
           response=json.dumps(data),
           sender=user.username,
           user_id=user.id
       )
       session.add(db_chat)
       session.commit()
       session.refresh(db_chat)
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
           detail=f"Database error: {str(e)}"
       )
   return data


@router.post("/sentiment_prediction", response_model=SentimentOutput)
def sentiment_prediction(
    inputs: SentimentInput, 
    user: User = Depends(get_current_user),
    session: Session = Depends(start_session)
    ) -> Dict[str, str]:  
    try:
        response = requests.post(SENTIMENT_ENDPOINT, json=inputs.model_dump())
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Prediction service error: {str(e)}"
            )
  
    try:
        db_chat = Predictions(
            response=json.dumps(data),
            sender=user.username,
            user_id=user.id
        )
        session.add(db_chat)
        session.commit()
        session.refresh(db_chat)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Database error: {str(e)}"
            )
    return data

@router.post("/qa_prediction", response_model=QAOutput)
def qa_prediction(
    inputs: QAInput, 
    user: User = Depends(get_current_user),
    session: Session = Depends(start_session)
    ) -> Dict[str, str]:  
    try:
        response = requests.post(QA_ENDPOINT, json=inputs.model_dump())
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Prediction service error: {str(e)}"
            )
    try:
        db_chat = Predictions(
            response=json.dumps(data),
            sender=user.username,
            user_id=user.id
        )
        session.add(db_chat)
        session.commit()
        session.refresh(db_chat)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Database error: {str(e)}"
            )
    return data