from mcp.server import InitializationOptions, NotificationOptions

from core.bases import AbstractStdioMcpServer


class FileServer(AbstractStdioMcpServer):
    def __init__(self):
        super().__init__()

    def create_initialization_options(self) -> InitializationOptions:
        return InitializationOptions(  # custom server init options
            server_name='file-server',
            server_version='0.0.1',
            capabilities=self.server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={}
            )
        )
