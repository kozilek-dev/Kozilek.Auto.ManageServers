from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from functools import lru_cache
from manager.server_manager import MinecraftManager, MinecraftBedRockServer
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(
    prefix="/servidores/backups",
    tags=["backups"],
)


universal_manager = MinecraftManager()


@router.post("/fazer/{name}")
async def make_backup(name: str, background_tasks: BackgroundTasks):
    server = universal_manager.get_server(name)
    if server is None:
        return JSONResponse(content={"mensagem": "Servidor não encontrado."}, status_code=404)
    background_tasks.add_task(universal_manager.backup_server, server)
    return JSONResponse(content={"mensagem": "Backup iniciado."}, status_code=200)

@router.post("/restaurar/{name}")
async def restore_backup(name: str, background_tasks: BackgroundTasks):
    server = universal_manager.get_server(name)
    if server is None:
        return JSONResponse(content={"mensagem": "Servidor não encontrado."}, status_code=404)
    
    backup_id = f'{name}.tar'
    background_tasks.add_task(universal_manager.restore_server, server, backup_id)
    return JSONResponse(content={"mensagem": "Restauração iniciada."}, status_code=200)