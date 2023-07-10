from fastapi import FastAPI

from app.db.database import create_database_if_not_exists, engine
from app.models.models import Base
from app.routers import login, projects, singup, tasks, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todoist Clone API")


@app.on_event("startup")
async def startup_event():
    create_database_if_not_exists()


app.include_router(singup.router, prefix="/api/v1")
app.include_router(login.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
