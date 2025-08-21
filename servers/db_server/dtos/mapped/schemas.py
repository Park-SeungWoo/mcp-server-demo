from pydantic import BaseModel


class Schemas(BaseModel):
    id: str
    type: str
