from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor
from mcp.types import Tool

from core.bases import AbstractTool
from core.utils.string_utils import snake_to_camel
from servers.stdio.db_server.dtos.mapped import *


class GetAllSchemasTool(AbstractTool):
    # @override
    @staticmethod
    def spec() -> Tool:
        return Tool(
            name="get_all_schemas_tool",
            description='Get all schemas available',
            inputSchema={
                'type': 'object',
                'properties': {},
            }
        )

    # @override
    @staticmethod
    async def execute() -> Any:
        with psycopg2.connect(
                host='127.0.0.1',
                port='5432',
                database='demo',
                user='jeremy',
                password='jeremy'
        ) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                result = GetAllSchemasTool.fetch_all(cur)
                return result

    @staticmethod
    def fetch_all(cur) -> dict:
        result: dict = {}
        cur.execute("select * from schemas")
        schema_dtos: list[Schemas] = [Schemas(**data) for data in cur.fetchall()]  # fetch all schemas
        for schema in schema_dtos:
            cur.execute(f"SELECT * FROM fields WHERE schema_id='{schema.id}'")
            field_dtos: list[Fields] = [Fields(**data) for data in cur.fetchall()]  # fetch all fields
            properties: dict = {}
            for field in field_dtos:
                properties[snake_to_camel(field.name)] = field.model_dump(
                    include={'type', 'description'})  # field_name -> fieldName
            result[schema.id] = {
                'type': schema.type,
                'properties': properties,
            }
        return result
