from fastapi import APIRouter, Depends, HTTPException, status

from .storage_service import base_storage_service

storage_router = APIRouter(prefix="/storage", tags=["storage"])


@storage_router.get("/")
async def getAllFolders():
    return base_storage_service.list_all_folders()
