class ResourceUriFormatException(ValueError):
    def __init__(self):
        super().__init__("Resource URI is invalid")