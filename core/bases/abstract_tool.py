from abc import ABCMeta, abstractmethod

from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource


class AbstractTool(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def spec() -> Tool:
        raise NotImplementedError("CustomTool.spec() is not implemented")

    @staticmethod
    @abstractmethod
    async def execute(**kwargs) -> list[TextContent | ImageContent | EmbeddedResource]:
        raise NotImplementedError("CustomTool.execute() is not implemented")
