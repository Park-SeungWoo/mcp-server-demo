from typing import Any

from mcp.types import Tool

from core.bases import AbstractTool


class PingPongTool(AbstractTool):
    @staticmethod
    def spec() -> Tool:
        return Tool(
            name='ping_pong_tool',  # must be snake_case of class name
            title='ping and pong',
            description='ping and pong pong pong',
            inputSchema={
                'type': 'object',
                'properties': {
                    'ping': {
                        'type': 'string',
                        'description': 'ping string',
                    }
                },
                'required': ['ping']
            }
        )

    @staticmethod
    async def execute(ping: str) -> Any:
        return {'pong': f"pingpong with {ping}"}
