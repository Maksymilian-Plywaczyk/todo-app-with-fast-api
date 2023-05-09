# TODO API USING FASTAPI

This project use FastAPI to create API for TODO list. The aim of the project is to learn about the FASTAPI framework and create a CRUD application to manage the TODO list. Among other things, the project includes user authentication. 
# Interactive API documentation
![api_todo](https://user-images.githubusercontent.com/65869609/226204948-7921f5a7-32d3-4f3a-ba20-7a711b610803.png)
## Getting started

 1. Create directory for this project and go to this folder:\
  `mkdir <your_directory_name>`\
  `cd <your_directory_name>`
 2. Clone the repository from GitHub (using HTPS):\
	`git clone https://github.com/Maksymilian-Plywaczyk/social_media_api.git`
 3. Create a virtual environment to isolate our package dependencies locally\
	 `python -m venv venv`\
	 `source venv/bin/activate` or on Windows `venv/Scripts/activate`
 4. Install list of dependencies from `requirements.txt`\
	`pip install -r requirements.txt`
 5. Create `.env` file i `app/` folder as the `.env.example` file and swap `SECRET KEY` with yours.
7. Run the project using [Docker configuration](#docker-configuration) and you should see the docs in url [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
8. Feel free to use this API :)

## Docker configuration
In order to run the project in a docker container you must run a `docker daemon` on your computer and then type command:
<br/>
`docker compose up --build`
<br/>
There are one container at this moment:
 -   Backend on port 8000 (name: `api_todo`)

Container is configurated to work as development environment so every change in api will trigger auto reload container. 
