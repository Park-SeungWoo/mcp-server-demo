from pydantic import BaseModel


class Schemas(BaseModel):
    api_id: int
    type: str
