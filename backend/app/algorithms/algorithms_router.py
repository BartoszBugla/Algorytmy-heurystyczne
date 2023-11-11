from fastapi import APIRouter, UploadFile, File

from .algorithms_service import algorithms_service

algorithms_router = APIRouter(prefix="/algorithms", tags=["algorithms"])


@algorithms_router.get("/{name}")
async def trigger_by_name(name: str, input: list[float]):
    return algorithms_service.trigger_by_name(name)


@algorithms_router.get("/")
async def read_all():
    """Get all functions"""
    return algorithms_service.read_all()


@algorithms_router.post("/{name}")
async def create(name: str, file: UploadFile = File(...)):
    return algorithms_service.create(name, file)


@algorithms_router.delete("/{name}")
async def delete_by_name(name: str):
    return algorithms_service.delete_by_name(name)
