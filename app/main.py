from fastapi import FastAPI
from routers import singup, login
import routers.user
from models import user
from db.database import engine

user.database.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(singup.router)
app.include_router(login.router)
app.include_router(routers.user.router)
