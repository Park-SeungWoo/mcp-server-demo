import asyncio
import argparse
import inspect

import servers
from core.bases import AbstractMcpServer
from core.utils.ansi_styler import ANSIStyler

SERVER_CLS: dict[str, type] = {
    k: v
    for k, v
    in inspect.getmembers(servers, inspect.isclass)
}
AVAIL_SERVER_OPTIONS: list[str] = [
    server.__name__
    for server in SERVER_CLS.values()
    if issubclass(server, AbstractMcpServer)
]


def parse_args():
    parser = argparse.ArgumentParser(description='Select a MCP server to start')
    parser.add_argument(
        '--server', '-S',
        choices=AVAIL_SERVER_OPTIONS,
        type=str,
        nargs=1,
        help='MCP server to start'
    )
    parser.add_argument(
        '--list', '-L',
        action='store_true',
        help='List available MCP servers'
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    if args.list:  # ls all servers
        print(ANSIStyler.style('Available MCP servers', fore_color='light-blue', font_style='bold'))
        for s in AVAIL_SERVER_OPTIONS:
            print(ANSIStyler.style(f"- {s}", fore_color='blue'))
    elif args.server:
        server_cls: type[AbstractMcpServer] = SERVER_CLS.get(args.server[0])
        asyncio.run(server_cls().run())
    else:
        print(ANSIStyler.style("Please select an available option", fore_color='red'))
