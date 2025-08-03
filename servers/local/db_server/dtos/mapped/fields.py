from pydantic import BaseModel


class Fields(BaseModel):
    id: int
    schema_id: int
    name: str
    type: str
    description: str
