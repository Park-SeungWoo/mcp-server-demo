from typing import Any

import psycopg2
from mcp.types import Tool

from core.bases import AbstractTool


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
            outputSchema={  # for structured output
                'type': 'object',
                'properties': {
                    'sample': {'type': 'string'},
                    'apis': {'type': 'array'}
                },
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
            cursor = conn.cursor()
            cursor.execute("select * from urls")
            return {
                "sample": "response",
                "urls": cursor.fetchall()
            }
