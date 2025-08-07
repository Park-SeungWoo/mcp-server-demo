import json

import uvicorn
from mcp.server.sse import SseServerTransport
from starlette.responses import Response
from starlette.applications import Starlette
from starlette.routing import Route

from core.bases import AbstractMcpServer
from core.utils.ansi_styler import ANSIStyler


class AbstractSSEMcpServer(AbstractMcpServer):
    async def handle_sse(self, request):
        transport = SseServerTransport("/message")

        async def message_handler():
            async for message in request.stream():
                data = await message
                # handle message
                yield f"data: {json.dumps({'response': data})}\n\n"

        return Response(
            message_handler(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
            }
        )

    async def run_server(self):
        print(ANSIStyler.style(f"MCP-{self.__class__.__name__} now running!",  # useless with stdio transport
                               fore_color='light-blue',
                               font_style='bold'
                               ))
        # print(ANSIStyler.style(str(self.create_initialization_options().model_dump_json(indent=2, exclude_none=True)),
        #                        fore_color='yellow'
        #                        ))

        app = Starlette(routes=[
            Route("/sse", self.handle_sse, methods=["POST"]),
        ])

        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        server_instance = uvicorn.Server(config)
        await server_instance.serve()
