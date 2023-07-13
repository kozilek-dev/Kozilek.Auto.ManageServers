from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from functools import lru_cache
from manager.server_manager import MinecraftManager, MinecraftBedRockServer
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(
    prefix="/servidores/logs",
    tags=["commands"],
)

def get_now() -> str:
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


universal_manager = MinecraftManager()


@router.get("/{name}")
async def view_logs(name: str, background_tasks: BackgroundTasks):
    retrieved_server = universal_manager.get_server(name)

    if retrieved_server is None:
        return JSONResponse({
            'resposta': 'Servidor não encontrado', 
            'executado_em': get_now()
        }, 404)

    logs = universal_manager.get_logs(retrieved_server)
    return JSONResponse(logs)

@router.get("/ultimo/{name}")
async def view_logs(name: str, background_tasks: BackgroundTasks):
    retrieved_server = universal_manager.get_server(name)

    if retrieved_server is None:
        return JSONResponse({
            'resposta': 'Servidor não encontrado', 
            'executado_em': get_now()
        }, 404)

    logs = universal_manager.get_last_log(retrieved_server)
    return JSONResponse(logs)