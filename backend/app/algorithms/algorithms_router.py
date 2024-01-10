from typing import Callable, List

from fastapi import APIRouter, UploadFile, File, Path, Query, Body, BackgroundTasks

from .algorithms_service import algorithms_service
from .algorithms_models import AlgorithmMetadata

algorithms_router = APIRouter(prefix="/algorithms", tags=["algorithms"])


@algorithms_router.post("/{name}/trigger")
def trigger(
    name: str = Path(..., description="The name of the algorithm to trigger"),
    fun: str = Query(..., description="The name of the function to use"),
    domain: List[List[float]] = Body(
        ...,
        description="domain for all dimnensions example: [[-5.12, 5.12], [-5.12, 5.12]]]",
    ),
    params: List[float] = Body(
        ...,
        description="The parameters for the algorithm if you don't know them check the Parama Info of given algorithm",
    ),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    background_tasks.add_task(algorithms_service.trigger_by_name, name, fun, domain, params)
    return {"status": f"solver started for algorithm {name}"}
    # return algorithms_service.trigger_by_name(name, fun, domain, params)


@algorithms_router.post("/{name}/trigger_test")
def trigger_test(
    name: str = Path(..., description="The name of the algorithm to trigger"),
    fun: str = Query(..., description="The name of the function to use"),
    domain: List[List[float]] = Body(
        ...,
        description="domain for all dimnensions example: [[-5.12, 5.12], [-5.12, 5.12]]]",
    ),
    params: List[List[float]] = Body(
        ...,
        description="The parameters for the algorithm in format [[range_start, range_end, step], [], etc.,"
                    "where next lists are the values for next parameters if you don't know the order of params"
                    "check algorithm's metadata",
    ),
):

    return algorithms_service.trigger_test_by_name(name, fun, domain, params)


@algorithms_router.get("/{name}")
def metadata(name: str) -> AlgorithmMetadata:
    return algorithms_service.read_algorithm_metadata(name)


@algorithms_router.get("/")
def read_all() -> list[str]:
    return algorithms_service.read_all()


@algorithms_router.post("/{name}")
def create(name: str, file: UploadFile = File(...)):
    return algorithms_service.create(name, file)


@algorithms_router.delete("/{name}")
def delete_by_name(name: str):
    return algorithms_service.delete_by_name(name)
