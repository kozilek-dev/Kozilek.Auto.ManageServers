from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from api.routers import actions, commands


async def not_found(request, exc):
    message = {"mensagem": "Oops! Recurso não foi encontrado."}
    return JSONResponse(content=message, status_code=404)

exceptions = {
    404: not_found,
}


app = FastAPI(exception_handlers=exceptions)
app.include_router(actions.router)
app.include_router(commands.router)