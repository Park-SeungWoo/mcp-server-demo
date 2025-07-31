from core.utils.ansi_styler import ANSIStyler


class McpPrimitiveImportError(ModuleNotFoundError):
    def __init__(self):
        super().__init__(
            ANSIStyler.style(
                'Please ensure that each mcp server follows this structure\n',
                fore_color='light-red'
            ) +
            ANSIStyler.style(
                '\t\t\t\t\tyour_mcp_server/\n'
                '\t\t\t\t\t\tprompts/\n'
                '\t\t\t\t\t\t\t__init__.py  <- Must import all implemented CustomPrompt classes here\n'
                '\t\t\t\t\t\tresources/\n'
                '\t\t\t\t\t\t\t__init__.py  <- Must import all implemented CustomResource classes here\n'
                '\t\t\t\t\t\ttools/\n'
                '\t\t\t\t\t\t\t__init__.py  <- Must import all implemented CustomTool classes here\n'
                '\t\t\t\t\t\tserver.py'
                '\t\t\t\t\t\t__init__.py'
                , fore_color='light-yellow'
            )
        )
