import routers.tasks
import routers.users
from db.database import engine
from fastapi import FastAPI
from models.models import Base
from routers import login, singup

# Create all the tables directly in the app
Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(singup.router)

app.include_router(login.router)
app.include_router(routers.users.router)
app.include_router(routers.tasks.router)
