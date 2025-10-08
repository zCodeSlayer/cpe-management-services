from fastapi import Request
from fastapi.responses import JSONResponse


async def handle_internal_provisioning_error(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "Internal provisioning exception",
        },
    )
