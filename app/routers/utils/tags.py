from enum import Enum


class Tags(str, Enum):
    users: str = "Users"
    tasks: str = "Tasks"
    login: str = "Login"
    register: str = "Registration"
