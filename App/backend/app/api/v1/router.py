# app/api/v1/router.py

from fastapi import APIRouter

from app.api.v1.master.material import router as material_router
from app.api.v1.master.suppliers import router as suppliers_router
from app.api.v1.system.dev_test.db_test import router as db_test_router

api_v1_router = APIRouter()

api_v1_router.include_router(material_router)

api_v1_router.include_router(suppliers_router)
api_v1_router.include_router(db_test_router)
