import asyncio
import re

from fastapi import APIRouter, Path, Body
from fastapi.responses import JSONResponse

from .base import API_PREFIX
from schemas import Configuration

router: APIRouter = APIRouter(prefix=f"{API_PREFIX}/equipment")


@router.post("/cpe/{id}")
async def activate_equipment(
    id: str = Path(...),
    configuration: Configuration = Body(...),
):
    if not re.match(r"^[a-zA-Z0-9]{6,}$", id):
        return JSONResponse(
            status_code=404,
            content={"code": 404, "message": "The requested equipment is not found"},
        )

    await asyncio.sleep(60)
    return JSONResponse(status_code=200, content={"code": 200, "message": "success"})
