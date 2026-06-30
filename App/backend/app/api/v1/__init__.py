from fastapi import APIRouter

from app.api.v1.master.material import router as material_router
from app.api.v1.master.supplier import router as suppliers_router
from app.api.v1.system.dev_test.db_test import router as db_test_router

router = APIRouter(prefix="/v1")
router.include_router(material_router)
router.include_router(suppliers_router)
router.include_router(db_test_router)
