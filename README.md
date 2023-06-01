# TODO API USING FASTAPI

This project use FastAPI to create API for TODO list. The aim of the project is to learn about the FASTAPI framework and create a CRUD application to manage the TODO list. Among other things, the project includes user authentication. 
# Interactive API documentation
![api_todo](https://user-images.githubusercontent.com/65869609/226204948-7921f5a7-32d3-4f3a-ba20-7a711b610803.png)
## Getting started

 1. Clone the repository from GitHub (using HTPS):\
	`git clone https://github.com/Maksymilian-Plywaczyk/todo-app-with-fast-api.git`
	<br/>
	Jump to directory `todo-app-with-fast-api/`
 2. Create a virtual environment to isolate our package dependencies locally\
	 `python -m venv venv`\
	 `source venv/bin/activate` or on Windows `venv/Scripts/activate`
 3. Install list of dependencies from `requirements.txt`\
	`pip install -r requirements.txt`
 4. Create `.env` file: `cp .env.template .env` and swap `SECRET KEY` with yours [Getting secret key](#getting-secret-key).
 5. Databases url for `SQLALCHEMY_DATABASE_URL` and `SQLALCHEMY_DATABASE_TEST_URL` are set by default but you can change names as you wish. Databases will be created after you run for the first time app.
6. In directory `todo-app-with-fast-api/` run command: `uvicorn app.main:app --reload`. Flag `--reload` enable user auto-reload for quicker development.
7. Feel free to use this API :)
8. You can also run project with Docker [Docker config](#docker-configuration)
## Docker configuration
In order to run the project in a docker container you must run a `docker daemon` on your computer and then type command:
<br/>
`docker compose up --build`
<br/>
There are one container at this moment:
 -   Backend on port 8000 (name: `api_todo`)

Container is configurated to work as development environment so every change in api will trigger auto reload container. 
<br/>
You should see the docs in url [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## GETTING SECRET KEY
To get secret key, which you need to pass in `.env` file you need to type in terminal that command and then copy this to `.env` file:
<br/>
`openssl rand -hex 32`
