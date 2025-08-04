from pydantic import BaseModel


class Fields(BaseModel):
    id: int
    schema_id: str
    name: str
    type: str
    description: str
