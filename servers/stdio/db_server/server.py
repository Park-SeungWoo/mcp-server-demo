from mcp.server import InitializationOptions, NotificationOptions

from core.bases import AbstractMcpServer


class DBServer(AbstractMcpServer):
    def __init__(self):
        super().__init__()

    def create_initialization_options(self) -> InitializationOptions:
        return InitializationOptions(
            server_name='local-db-server',
            server_version='0.0.1',
            capabilities=self.server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={}
            )
        )

"""
TODO: tool의 실행부에 commit 전 확인 과정 필요
"""
