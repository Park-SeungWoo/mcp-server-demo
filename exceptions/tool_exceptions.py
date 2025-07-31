class ToolNotExistException(ValueError):
    def __init__(self, tool_name: str):
        super().__init__(f"Tool name [{tool_name}] is not exists")