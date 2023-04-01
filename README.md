# TODO API USING FASTAPI

This project use FastAPI to create API for TODO list. The aim of the project is to learn about the FASTAPI framework and create a CRUD application to manage the TODO list. Among other things, the project includes user authentication. 
# Interactive API documentation
![api_todo](https://user-images.githubusercontent.com/65869609/226204948-7921f5a7-32d3-4f3a-ba20-7a711b610803.png)
## How to configurate environment
Create an virtual environment:
<br/>
`python -m venv venv` 

Activate your venv:
<br/>
`#Windows
/venv/Scripts/activate`

`#Linux
source /venv/bin/activate `

Install requirements:
<br/>
`pip install --no-cache-dir --upgrade -r ./app/requirements.txt`
## How to use it
`git clone https://github.com/Maksymilian-Plywaczyk/todo-app-with-fast-api.git`

Open your terminal and pass:
<br/>
`uvicorn main:app --reload` 

Go to:
<br/>
`localhost:8000/docs`
