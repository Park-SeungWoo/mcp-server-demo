import random
from typing import Any

from mcp.types import Tool

from core.bases import AbstractMcpServer


class DynamicToolManagementServer(AbstractMcpServer):
    def __init__(self) -> None:
        super().__init__()
        self.db_connection = None  # TODO: DB connection

    def set_handlers(self):
        # TODO: must set prompt, resources also
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            # TODO: get JSON formatted tool spec data from database
            tool1: Tool = Tool(
                name='first_tool',
                description='first tool',
                inputSchema={
                    'type': 'object',
                    'properties': {
                        'ping': {
                            'type': 'string',
                            'description': 'ping string',
                            'default': 'MCP'
                        }
                    },
                    'required': ['ping']
                }
            )
            tool2: Tool = Tool(
                name='second_tool',
                description='second tool',
                inputSchema={
                    'type': 'object',
                    'properties': {
                        'ping': {
                            'type': 'string',
                            'description': 'ping string',
                            'default': 'SSE'
                        }
                    },
                    'required': ['ping']
                }
            )
            return [tool1] if random.random() < 0.5 else [tool2]

        @self.server.call_tool()
        async def call_tool(tool_name: str, kwargs: dict) -> Any:
            # TODO: handle tool by its name
            # get api spec from database by tool_name and call it
            return {
                'pong': tool_name,
                'received': kwargs
            }
