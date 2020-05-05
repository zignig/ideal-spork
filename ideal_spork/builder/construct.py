# Choose a construct for the board

from ..logger import logger

log = logger(__name__)


def interactive_construct(available):
    log.critical("List choose %s", str(available))


def choose_construct(available, constr, board):
    log.critical(available)
    log.critical(constr)
    log.critical(board)
