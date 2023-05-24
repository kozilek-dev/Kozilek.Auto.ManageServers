from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from functools import lru_cache
from manager.server_manager import MinecraftManager, MinecraftBedRockServer
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(
    prefix="/servidores/comandos",
    tags=["commands"],
)

@lru_cache()
def get_now() -> str:
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


universal_manager = MinecraftManager()



class CommandRequest(BaseModel):
    servidor: str
    comando: str


class PropertyRequest(BaseModel):
    servidor: str
    propriedade: str
    valor: str


@router.post('/')
async def run_command(command_request: CommandRequest):
    server = MinecraftBedRockServer(command_request.servidor)
    container = universal_manager.create_server(server)
    response = universal_manager.run_command(container, command_request.comando)
    return JSONResponse(
        {
            'resposta': response,
            'executado_em': get_now()
        }, 200)

@router.post('/sem-resposta')
async def run_command_without_response(command_request: CommandRequest, background_tasks: BackgroundTasks):
    server = MinecraftBedRockServer(command_request.servidor)
    container = universal_manager.create_server(server)
    background_tasks.add_task(universal_manager.run_command, container, command_request.comando)
    return JSONResponse({
            'resposta': 'Comando executado', 
            'executado_em': get_now()
        }, 202)

@router.put('/propriedades')
async def set_property(command_request: PropertyRequest, background_tasks: BackgroundTasks):
    server = MinecraftBedRockServer(command_request.servidor)
    container = universal_manager.create_server(server)
    background_tasks.add_task(universal_manager.set_server_property, container, command_request.propriedade, command_request.valor)
    return JSONResponse({
            'resposta': f'Propriedade {command_request.propriedade} definida para {command_request.valor}', 
            'executado_em': get_now()
        }, 202)
