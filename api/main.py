import jobs
from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from api.routers import actions, commands, backups, logs
from fastapi.middleware.cors import CORSMiddleware


async def not_found(request, exc):
    message = {"mensagem": "Ih rapaz, deu xabu"}
    return JSONResponse(content=message, status_code=404)

exceptions = {
    404: not_found,
}

r = jobs.Runner()
r.add_job(jobs.BackupContainersJob(2, 0, 0))
r.add_job(jobs.UpdateContainersJob(12, 0, 0))
r.start()


app = FastAPI(exception_handlers=exceptions)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(actions.router)
app.include_router(commands.router)
app.include_router(backups.router)
app.include_router(logs.router)