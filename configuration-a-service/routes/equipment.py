import asyncio

from fastapi import APIRouter, Path, Body
from fastapi.responses import JSONResponse

from .base import API_PREFIX
from schemas import Configuration

router: APIRouter = APIRouter(prefix=f"{API_PREFIX}/equipment")


@router.post("/cpe/{id}")
async def activate_equipment(
    id: str = Path(..., regex=r"^[a-zA-Z0-9]{6,}$"),
    configuration: Configuration = Body(...),
):
    await asyncio.sleep(60)
    return JSONResponse(status_code=200, content={"code": 200, "message": "success"})
