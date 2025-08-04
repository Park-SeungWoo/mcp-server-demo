from pydantic import BaseModel


class Urls(BaseModel):
    id: int
    host: str
    port: str
    description: str
