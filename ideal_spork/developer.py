# development command line tools

from .logger import logger

log = logger(__name__)


def developer_tooling(action):
    log.info("Developer tooling")
    development_parser = action.add_parser("tools", help="Development Commands")
    tools = development_parser.add_subparsers(dest="tool")
