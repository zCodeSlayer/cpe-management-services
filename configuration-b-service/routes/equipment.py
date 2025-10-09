import asyncio
import re
import json
import uuid
from redis.asyncio import Redis

from fastapi import APIRouter, Depends, Path, Body
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from .base import API_PREFIX
from schemas import Configuration
from dependencies import get_redis, get_rabbitmq_connection
from dependencies.rabbitmq import RabbitMQService

router: APIRouter = APIRouter(prefix=f"{API_PREFIX}/equipment")


@router.post("/cpe/{id}")
async def activate_equipment(
    id: str = Path(...),
    configuration: Configuration = Body(...),
    rabbitmq_client: RabbitMQService = Depends(get_rabbitmq_connection),
    redis_client: Redis = Depends(get_redis),
):
    if not re.match(r"^[a-zA-Z0-9]{6,}$", id):
        return JSONResponse(
            status_code=404,
            content={"code": 404, "message": "The requested equipment is not found"},
        )

    task_id: str | None = None
    while True:
        task_id = uuid.uuid4().hex
        key = f"equipment:{id}:task:{task_id}"
        created = await redis_client.set(key, "IN_PROGRESS", nx=True)
        if created:
            break

    rabbitmq_message: str = json.dumps(
        {
            "equipmentId": id,
            "taskId": task_id,
            "configuration": configuration.model_dump(by_alias=True),
        }
    )
    await rabbitmq_client.send_message(
        queue_name="externally_configured_queue_1", message=rabbitmq_message
    )

    return JSONResponse(status_code=200, content={"code": 200, "taskId": f"{task_id}"})


@router.get("/cpe/{id}/task/{task}")
async def check_task_status(
    id: str = Path(...),
    task: str = Path(...),
    redis_client: Redis = Depends(get_redis),
):
    pattern = f"equipment:{id}*"
    cursor: int = 0
    cursor, _ = await redis_client.scan(cursor, match=pattern, count=5)

    if not cursor:
        return JSONResponse(
            status_code=404,
            content={"code": 404, "message": "The requested equipment is not found"},
        )

    task_status: str | None = await redis_client.get(f"equipment:{id}:task:{task}")
    if task_status is None:
        return JSONResponse(
            status_code=404,
            content={"code": 404, "message": "The requested task is not found"},
        )

    if task_status == "IN_PROGRESS":
        return JSONResponse(
            status_code=204,
            content={"code": 204, "message": "Task is still running"},
        )

    if task_status == "DONE":
        return JSONResponse(
            status_code=200,
            content={"code": 200, "message": "Completed"},
        )

    raise HTTPException
