from fastapi import FastAPI

from app.db.database import create_database_if_not_exists, engine
from app.models.models import Base
from app.routers import login, singup, tasks, users

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    create_database_if_not_exists()


app.include_router(singup.router)

app.include_router(login.router)
app.include_router(users.router)
app.include_router(tasks.router)
