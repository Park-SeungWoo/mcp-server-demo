import asyncio

from servers.local.file_server.server import FileServer

asyncio.run(FileServer().run())
