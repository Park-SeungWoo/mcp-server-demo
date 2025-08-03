import asyncio
import argparse

from core.utils.ansi_styler import ANSIStyler
from servers.local.file_server.server import FileServer
from servers.local.db_server.server import DBServer

AVAIL_SERVER_OPTIONS: list[str] = ['file', 'db']  # TODO: dynamically find existing servers


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
        server = args.server[0]
        match server:
            case 'file':
                server = FileServer()
            case 'db':
                server = DBServer()
        asyncio.run(server.run())
    else:
        print(ANSIStyler.style("Please select an available option", fore_color='red'))
