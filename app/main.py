import routers.tasks
import routers.users
from db.database import engine
from fastapi import FastAPI
from models import tasks, users
from routers import login, singup

users.database.Base.metadata.create_all(bind=engine)
tasks.database.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(singup.router)
app.include_router(login.router)
app.include_router(routers.users.router)
app.include_router(routers.tasks.router)
