from fastapi import APIRouter
from app.api import Test_Router, API_V1_Router

router = APIRouter()

router.include_router(Test_Router)
router.include_router(API_V1_Router)