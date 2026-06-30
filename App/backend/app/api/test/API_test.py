from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/test")
async def test_get(request: Request):
    return {
        "message": "GET request received",
        "query_params": dict(request.query_params),
        "headers": dict(request.headers),
    }


@router.post("/test")
async def test_post(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = None

    return {
        "message": "POST request received",
        "query_params": dict(request.query_params),
        "body": body,
        "headers": dict(request.headers),
    }
