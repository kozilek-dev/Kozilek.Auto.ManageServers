from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from functools import lru_cache
from manager.server_manager import MinecraftManager, MinecraftBedRockServer
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

router = APIRouter(
    prefix="/servidores/acoes",
)


universal_manager = MinecraftManager()


def get_now() -> str:
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')

class ServerProperties(BaseModel):
    server_name: str
    gamemode: str
    force_gamemode: bool
    difficulty: str
    allow_cheats: bool
    max_players: int
    online_mode: bool
    allow_list: bool
    server_port: Optional[int] = None
    server_portv6: Optional[int] = None
    view_distance: int
    tick_distance: int
    player_idle_timeout: int
    max_threads: int
    level_name: str
    level_seed: str
    default_player_permission_level: str
    texturepack_required: bool
    content_log_file_enabled: bool
    compression_threshold: int
    server_authoritative_movement: str
    player_movement_score_threshold: int
    player_movement_action_direction_threshold: float
    player_movement_distance_threshold: float
    player_movement_duration_threshold_in_ms: int
    correct_player_movement: bool
    server_authoritative_block_breaking: bool
    EULA: bool = True


@router.post("/")
async def create(server_properties: ServerProperties, background_tasks: BackgroundTasks):
    server = MinecraftBedRockServer(server_properties.server_name, server_properties)
    background_tasks.add_task(universal_manager.create_server, server)
    return JSONResponse({
            'resposta': 'Servidor criado',
            'executado_em': get_now()
        }, 202)

@router.get("/{name}")
async def get(name: str):
    container = universal_manager.get_server(name)

    if container is None:
        return JSONResponse({
            'resposta': 'Servidor não encontrado', 
            'executado_em': get_now()
        }, 404)

    return JSONResponse({
            'id':  container.id, 
            'porta': universal_manager.get_server_port(container),  
            'nome': container.name,
            'status': container.status,
            'saudavel': universal_manager.is_healthy(container),
            'executado_em': get_now()
        }, 200)

@router.get("/{name}/desempenho")
async def get_performance(name: str):
    container = universal_manager.get_server(name)
    performance_stats = universal_manager.get_performance_stats(container)

    if performance_stats is None:
        return JSONResponse({
            'resposta': 'Servidor não está rodando e/ou não possui estatísticas de desempenho', 
            'executado_em': get_now()
        }, 404)

    if container is None:
        return JSONResponse({
            'resposta': 'Servidor não encontrado', 
            'executado_em': get_now()
        }, 404)
    
    

    return JSONResponse(performance_stats, 200)

    
@router.delete("/{name}")
async def delete(name: str, background_tasks: BackgroundTasks):
    retrieved_server = universal_manager.get_server(name)
    background_tasks.add_task(universal_manager.delete_server, retrieved_server)
    return JSONResponse(
        {
            'resposta': 'Ação executada', 
            'executado_em': get_now()
        }, 202)

@router.delete("/")
async def delete(background_tasks: BackgroundTasks):
    background_tasks.add_task(universal_manager.delete_all_servers)
    return JSONResponse(
        {
            'resposta': 'Ação executada', 
            'executado_em': get_now()
        }, 202)

@router.get("/")
async def list():
    servers = universal_manager.get_all_servers()
    servers_name = [{
        'id':  server.id,
        'nome': server.name, 
        'porta': universal_manager.get_server_port(server), 
        'saudavel': universal_manager.is_healthy(server),
        'status': server.status
    } for server in servers]
    return JSONResponse(
        {
            'servidores': servers_name, 
            'executado_em': get_now()
        }, 200)

@router.get("/{name}/mundos")
async def list_worlds(name: str):
    retrieved_server = universal_manager.get_server(name)
    worlds = universal_manager.get_all_worlds(retrieved_server)
    return JSONResponse(
        {
            'mundos': worlds, 
            'executado_em': get_now()
        }, 200)

@router.put("/iniciar/{name}")
async def start(name: str, background_tasks: BackgroundTasks):
    retrieved_server = universal_manager.get_server(name)
    background_tasks.add_task(universal_manager.start_server, retrieved_server)
    return JSONResponse({
            'resposta': 'Ação executada', 
            'executado_em': get_now()
        }, 202)

@router.put("/parar/{name}")
async def stop(name: str, background_tasks: BackgroundTasks):
    retrieved_server = universal_manager.get_server(name)
    background_tasks.add_task(universal_manager.stop_server, retrieved_server)
    return JSONResponse({
            'resposta': 'Ação executada', 
            'executado_em': get_now()
        }, 202)

@router.put("/reiniciar/{name}")
async def restart(name: str, background_tasks: BackgroundTasks):
    retrieved_server = universal_manager.get_server(name)
    background_tasks.add_task(universal_manager.restart_server, retrieved_server)
    return JSONResponse({
            'resposta': 'Ação executada', 
            'executado_em': get_now()
        }, 202)

@router.put("/atualizar/{name}")
async def update(name: str, background_tasks: BackgroundTasks):
    retrieved_server = universal_manager.get_server(name)
    background_tasks.add_task(universal_manager.update_server, retrieved_server)
    return JSONResponse({
            'resposta': 'Ação executada', 
            'executado_em': get_now()
        }, 202)