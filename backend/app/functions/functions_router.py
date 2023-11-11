from fastapi import APIRouter, UploadFile, File

from .functions_service import functions_service

functions_router = APIRouter(prefix="/functions", tags=["functions"])


@functions_router.post("/{name}/trigger")
async def trigger_by_name(name: str, input: list[float]):
    """Trigger function by name."""
    return functions_service.trigger_by_name(name, input)


@functions_router.get("/")
async def read_all():
    """Get all functions"""
    return functions_service.read_all()


@functions_router.post("/{name}")
async def create(name: str, file: UploadFile = File(...)):
    return functions_service.create(name, file)


@functions_router.delete("/{name}")
async def delete_by_name(name: str):
    return functions_service.delete_by_name(name)
