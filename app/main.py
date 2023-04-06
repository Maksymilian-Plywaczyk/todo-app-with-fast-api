from fastapi import FastAPI

from app.db.database import engine
from app.models.models import Base
from app.routers import login, singup, tasks, users

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(singup.router)

app.include_router(login.router)
app.include_router(users.router)
app.include_router(tasks.router)
