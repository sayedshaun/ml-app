from fastapi import APIRouter, status
from typing import Dict
from schema.output import JsonResponse


router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK, response_model=JsonResponse)
def root() -> str:
   return {"message": "running"}

@router.get("/healthcheck", status_code=status.HTTP_200_OK, response_model=JsonResponse)
def health_check() -> JsonResponse:
   return {"message": "ok"}

