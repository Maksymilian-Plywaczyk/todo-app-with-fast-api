from pydantic import BaseModel


class CollaboratorProperties(BaseModel):
    id: int
    name: str
    email: str


class Collaborator(BaseModel):
    collaborator: CollaboratorProperties
