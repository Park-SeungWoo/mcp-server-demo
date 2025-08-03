from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor
from mcp.types import Tool

from core.bases import AbstractTool
from servers.local.db_server.dtos.mapped import *
from servers.local.db_server.dtos.responses.api_spec_structured_output import ApiSpecDto, EndpointSpecDto, SchemaDto


class GetAllSchemasTool(AbstractTool):
    # @override
    @staticmethod
    def spec() -> Tool:
        return Tool(
            name="get_all_schemas_tool",
            description='Get all schemas available to call an api.',
            inputSchema={
                'type': 'object',
                'properties': {},
            },
            outputSchema={  # TODO: validate this structure, it's not match with real output
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'url': {'type': 'string'},
                        'description': {'type': 'string'},
                        'endpoints': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'method': {'type': 'string'},
                                    'path': {'type': 'string'},
                                    'description': {'type': 'string'},
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'type': {'type': 'string'},
                                            'properties': {
                                                'type': 'object',
                                                'additionalProperties': {
                                                    'type': 'object',
                                                    'properties': {
                                                        'type': {'type': 'string'},
                                                        'description': {'type': 'string'}
                                                    },
                                                    'required': ['type', 'description']
                                                }
                                            }
                                        },
                                        'required': ['type', 'properties']
                                    }
                                },
                                'required': ['method', 'path', 'description', 'schema']
                            }
                        }
                    },
                    'required': ['url', 'description', 'endpoints']
                }
            }
        )

    # @override


    @staticmethod
    def __fetch_all(cur) -> list[BaseModel]:
        result: list = []
        cur.execute("select * from urls")
        urls: list[Urls] = [Urls(**data) for data in cur.fetchall()]
        for url in urls:  # fetch all urls
            cur.execute(f"select * from apis where url_id={url.id}")
            apis: list[Apis] = [Apis(**data) for data in cur.fetchall()]
            endpoints: list = []
            for api in apis:  # endpoints per base urls
                cur.execute(f"select * from schemas where api_id={api.id}")
                schema: Schemas = Schemas(**cur.fetchall()[0])  # fetch schema info
                cur.execute(f"select * from fields where schema_id={schema.api_id}")
                fields: list[Fields] = [Fields(**data) for data in cur.fetchall()]
                print(fields)
                schema_dto: SchemaDto = SchemaDto(
                    type=schema.type,
                    properties={field.name: {
                        'type': field.type,
                        'description': field.description
                    } for field in fields},
                )
                endpoints.append(
                    EndpointSpecDto(
                        method=api.method,
                        path=api.path,
                        description=api.description,
                        schema=schema_dto,
                    )
                )
            result.append(
                ApiSpecDto(
                    url=url.url,
                    description=url.description,
                    endpoints=endpoints
                )
            )
        return result
