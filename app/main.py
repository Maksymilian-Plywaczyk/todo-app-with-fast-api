from fastapi import FastAPI
from routers import singup
from models import user
from db.database import engine

user.database.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(singup.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
