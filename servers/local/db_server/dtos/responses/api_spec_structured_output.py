from pydantic import BaseModel


class ApiSpecDto(BaseModel):
    url: str
    description: str
    endpoints: list['EndpointSpecDto']

class EndpointSpecDto(BaseModel):
    key: str
    method: str
    path: str
    description: str
    schema: 'SchemaDto'

class SchemaDto(BaseModel):
    type: str
    properties: dict