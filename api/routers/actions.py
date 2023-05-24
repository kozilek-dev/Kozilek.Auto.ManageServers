from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
from functools import lru_cache
from manager.server_manager import MinecraftManager, MinecraftBedRockServer
from datetime import datetime

router = APIRouter(
    prefix="/servidores/acoes",
)


universal_manager = MinecraftManager()


@lru_cache()
def get_now() -> str:
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


@router.post("/{name}")
async def create(name: str):
    server = MinecraftBedRockServer(name)
    container = universal_manager.create_server(server)
    return JSONResponse({
            'id':  container.id, 
            'porta': universal_manager.get_server_port(container),  
            'nome': container.name,
            'saudavel': universal_manager.is_healthy(container),
            'executado_em': get_now()
        }, 201)

@router.get("/{name}")
async def get(name: str):
    container = universal_manager.get_server(name)
    return JSONResponse({
            'id':  container.id, 
            'porta': universal_manager.get_server_port(container),  
            'nome': container.name,
            'status': container.status,
            'saudavel': universal_manager.is_healthy(container),
            'executado_em': get_now()
        }, 200)
    
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
        'status': server.status,
        'saudavel': universal_manager.is_healthy(server)
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