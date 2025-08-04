from pydantic import BaseModel


class Apis(BaseModel):
    id: int
    url_id: int
    key: str
    path: str
    method: str
    description: str
