import logging

from fastapi import APIRouter, status


logger = logging.getLogger(__name__)

healthcheck_router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
)


@healthcheck_router.get("/", status_code=status.HTTP_200_OK)
async def get_status() -> dict[str, str]:
    logger.debug("Healthcheck endpoint called")
    return {"message": "ok"}
