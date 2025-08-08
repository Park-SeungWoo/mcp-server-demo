from abc import ABCMeta
import asyncio
import inspect
from typing import Any

import uvicorn
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.responses import Response
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Prompt, Resource, Tool, GetPromptResult
from pydantic import AnyUrl

from core.enums.transport_enums import TransportEnum
from core.utils.ansi_styler import ANSIStyler
from exceptions.errors import McpPrimitiveImportError
from exceptions.tool_exceptions import ToolNotExistException
from core.bases.abstract_tool import AbstractTool
from core.utils import string_utils as strutil


class AbstractMcpServer(metaclass=ABCMeta):
    def __init__(self):
        self.server: Server = Server(f"{strutil.pascal_to_snake(self.__class__.__name__)}")

    def __dynamic_import(self):
        from pathlib import Path
        import sys

        base_path = Path(inspect.getfile(self.__class__)).parent.absolute()
        try:
            sys.path.append(str(base_path))

            self.tools = __import__('tools')
            self.resources = __import__('resources')
            self.prompts = __import__('prompts')
        except ModuleNotFoundError:
            raise McpPrimitiveImportError()
        finally:
            sys.path.remove(str(base_path))

    def set_handlers(self):
        self.__dynamic_import()

        @self.server.list_prompts()
        async def list_prompts() -> list[Prompt]:
            pass

        @self.server.get_prompt()
        async def get_prompt(name: str, kwargs: dict) -> GetPromptResult:
            pass

        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            pass

        @self.server.read_resource()
        async def read_resource(uri: AnyUrl) -> str:
            pass

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            tool_cls: list = inspect.getmembers(self.tools, inspect.isclass)
            return [tool.spec() for _, tool in tool_cls if issubclass(tool, AbstractTool)]

        @self.server.call_tool()
        async def call_tool(name: str, kwargs: dict) -> Any:
            tool: AbstractTool = getattr(self.tools, strutil.snake_to_pascal(name), None)
            if tool:  # TODO: argument exception handling
                return await tool.execute(**kwargs)
            raise ToolNotExistException(name)

    def create_initialization_options(self) -> InitializationOptions:
        return self.server.create_initialization_options()

    def run(self, transport: TransportEnum):
        self.set_handlers()
        match transport:
            case TransportEnum.STDIO:
                self.run_stdio()
            case TransportEnum.SSE:
                self.run_sse()

    def run_stdio(self):
        asyncio.run(self.__stdio())

    def run_sse(self):
        print(ANSIStyler.style(f"[MCP-SSE] {self.__class__.__name__} now running!",  # useless with stdio transport
                               fore_color='light-blue',
                               font_style='bold'
                               ))
        # print(ANSIStyler.style(str(self.create_initialization_options().model_dump_json(indent=2, exclude_none=True)),
        #                        fore_color='yellow'
        #                        ))
        uvicorn.run(self.__sse(), host='0.0.0.0', port=8080)

    async def __stdio(self):
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.create_initialization_options()
            )

    def __sse(self) -> Starlette:
        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
                await self.server.run(
                    streams[0], streams[1], self.server.create_initialization_options()
                )
            return Response()

        return Starlette(
            debug=True,
            routes=[
                Route('/sse', endpoint=handle_sse, methods=['GET']),
                Mount('/messages/', app=sse.handle_post_message),
            ]
        )
