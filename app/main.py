from fastapi import FastAPI

from app.routers import login, projects, sections, singup, tasks, users
from app.routers.utils.prefixes import APIPrefixes

app = FastAPI(title="Todoist Clone API")


# @app.on_event("startup")
# async def startup_event():
#     create_database_if_not_exists()


app.include_router(singup.router, prefix=APIPrefixes.version)
app.include_router(login.router, prefix=APIPrefixes.version)
app.include_router(users.router, prefix=APIPrefixes.version)
app.include_router(tasks.router, prefix=APIPrefixes.version)
app.include_router(projects.router, prefix=APIPrefixes.version)
app.include_router(sections.router, prefix=APIPrefixes.version)
