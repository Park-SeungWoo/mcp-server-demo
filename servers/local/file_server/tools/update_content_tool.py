from typing import Any

from mcp.types import Tool

from core.bases import AbstractTool


class UpdateContentTool(AbstractTool):
    # @override
    @staticmethod
    def spec() -> Tool:
        return Tool(
            name='update_content_tool',  # must be snake_case of class name
            title='file content updater',
            description='Update file content with user input',
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
                        'maxLength': 50,
                        'minLength': 1,
                    }
                },
                'required': ['file_name', 'content']
            },
            outputSchema={  # for structured output
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'prev_content': {'type': 'string'}
                },
                'required': ['status', 'prev_content']
            }
        )

    # @override
    @staticmethod
    async def execute(file_name: str, content: str) -> Any:
        prev: str = ''
        with open(file_name, 'r') as f:
            prev = '\n'.join(f.readlines())
        with open(file_name, 'w') as f:
            f.write(content)
        return {
            'status': True,
            'prev_content': prev,
        }
