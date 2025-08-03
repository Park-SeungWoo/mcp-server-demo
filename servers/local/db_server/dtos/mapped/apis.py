from pydantic import BaseModel


class Apis(BaseModel):
    id: int
    url_id: int
    path: str
    method: str
    description: str
