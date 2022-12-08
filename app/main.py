from fastapi import FastAPI
from routers import singup, login
import routers.users
from models import users
from db.database import engine

users.database.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(singup.router)
app.include_router(login.router)
app.include_router(routers.users.router)
