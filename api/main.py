import jobs
from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from api.routers import actions, commands, backups, logs


async def not_found(request, exc):
    message = {"mensagem": "Oops! Recurso não foi encontrado."}
    return JSONResponse(content=message, status_code=404)

exceptions = {
    404: not_found,
}

r = jobs.Runner()
r.add_job(jobs.PurgeContainersJob(1, 0, 0))
r.add_job(jobs.BackupContainersJob(2, 0, 0))
r.add_job(jobs.UpdateContainersJob(12, 0, 0))
r.start()


app = FastAPI(exception_handlers=exceptions)
app.include_router(actions.router)
app.include_router(commands.router)
app.include_router(backups.router)
app.include_router(logs.router)