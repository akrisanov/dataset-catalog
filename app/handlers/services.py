from fastapi import APIRouter

from app.schemas.response import Message


services_router = APIRouter()


@services_router.get(
    "/",
    response_model=Message,
    summary="Check whether the web service running",
    description="This API endpoint can serve for Kubernetes liveness probe.",
)
async def healthcheck():
    return {"detail": "OK"}
