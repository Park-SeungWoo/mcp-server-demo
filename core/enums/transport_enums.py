import enum


class TransportEnum(enum.Enum):
    # reserved
    SSE = 'sse'
    STDIO = 'stdio'
    # STREAMABLEHTTP = 'streamablehttp'

    @staticmethod
    def all() -> list:
        return list(TransportEnum)


if __name__ == '__main__':
    print(list(map(lambda x: x.value, TransportEnum.all())))
    print(TransportEnum('sse'))  # by value
    print(TransportEnum['SSE'])  # by enum name