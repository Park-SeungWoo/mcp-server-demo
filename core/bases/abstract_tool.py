from abc import ABCMeta, abstractmethod
from typing import Any

from mcp.types import Tool


class AbstractTool(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def spec() -> Tool:
        raise NotImplementedError("CustomTool.spec() is not implemented")

    @staticmethod
    @abstractmethod
    async def execute(**kwargs) -> Any:
        raise NotImplementedError("CustomTool.execute() is not implemented")
