from mcp import Tool
from mcp.types import TextContent, ImageContent, EmbeddedResource

from core.bases import AbstractTool

class UpdateContentTool(AbstractTool):
    # @override
    @staticmethod
    def spec() -> Tool:
        return Tool(
            name='update_content_tool',
            description='Update file content',
            inputSchema={
                'type': 'object',
                'properties': {
                    'file_name': {
                        'type': 'string',
                        'description': 'File name',
                    },
                    'content': {
                        'type': 'string',
                        'description': 'File content',
                        'maxLength': 10,
                        'minLength': 1,
                    }
                },
                'required': ['file_name', 'content']
            }
        )

    # @override
    @staticmethod
    async def execute(file_name: str, content: str) -> list[TextContent | ImageContent | EmbeddedResource]:
        with open(file_name, 'w') as f:
            f.write(content)
        return []  # response objects
