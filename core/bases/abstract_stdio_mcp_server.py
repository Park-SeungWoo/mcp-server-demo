from mcp import stdio_server

from core.bases import AbstractMcpServer


class AbstractStdioMcpServer(AbstractMcpServer):
    async def run_server(self):
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.create_initialization_options()
            )
