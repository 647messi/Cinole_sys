from fastapi import APIRouter

from app.api.v1.master.raw_material_dict import router as raw_material_dict_router
from app.api.v1.master.supplier import router as suppliers_router
from app.api.v1.system.dev_test.db_test import router as db_test_router

router = APIRouter(prefix="/v1")
router.include_router(raw_material_dict_router)
router.include_router(suppliers_router)
router.include_router(db_test_router)
