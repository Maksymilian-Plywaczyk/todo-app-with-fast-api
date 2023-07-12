from enum import Enum


class APIPrefixes(str, Enum):
    version: str = "/api/v1"
    users: str = "/users"
    tasks: str = "/tasks"
    projects: str = "/projects"
    sections: str = "/sections"
