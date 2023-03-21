from enum import Enum


class Tags(str, Enum):
    users: str = "Users"
    tasks: str = "Tasks"
    login: str = "Login"
    register: str = "Registration"
    reset_password: str = "Reset user password"
