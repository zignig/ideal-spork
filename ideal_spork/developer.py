# development command line tools

from .logger import logger

log = logger(__name__)


def developer_tooling(parser):
    log.critical("No developer tooling")
