from pydantic import BaseModel


class Urls(BaseModel):
    id: int
    url: str
    description: str
