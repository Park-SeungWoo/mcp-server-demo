from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor
from mcp.types import Tool

from core.bases import AbstractTool
from core.utils.string_utils import snake_to_camel
from servers.local.db_server.dtos.mapped import *


class GetSpecificSchemaTool(AbstractTool):
    # @override
    @staticmethod
    def spec() -> Tool:
        return Tool(
            name="get_specific_schema_tool",
            description='Get specific schema via schema id',
            inputSchema={
                'type': 'object',
                'properties': {
                    'schema_id': {'type': 'string'},
                },
            }
        )

    # @override
    @staticmethod
    async def execute(schema_id: str) -> Any:
        with psycopg2.connect(
                host='127.0.0.1',
                port='5432',
                database='demo',
                user='jeremy',
                password='jeremy'
        ) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                schema: dict = GetSpecificSchemaTool.fetch(cur, schema_id)
                return {'schema': schema}

    @staticmethod
    def fetch(cur, schema_id: str) -> dict:
        result: dict = {}
        cur.execute(f"select * from schemas where id = '{schema_id}'")
        schema_dtos: list[Schemas] = [Schemas(**data) for data in cur.fetchall()]  # fetch schema
        properties: dict = {}
        for schema in schema_dtos:
            cur.execute(f"SELECT * FROM fields WHERE schema_id='{schema.id}'")
            field_dtos: list[Fields] = [Fields(**data) for data in cur.fetchall()]  # fetch all fields
            for field in field_dtos:
                properties[snake_to_camel(field.name)] = field.model_dump(
                    include={'type', 'description'})  # field_name -> fieldName
        result['type'] = schema_dtos[0].type
        result['properties'] = properties
        return result
