# Maps devices and peripherals to a board
from ..logger import logger

log = logger(__name__)

from ..peripheral import *
from ..utils import search


def get_resources(board_instance):
    res = list(board_instance.resources.keys())
    res_names = set()
    for i in res:
        res_names.add(i[0])
    log.critical(search.catalog.sections)
    for r in res_names:
        if r in search.catalog.sections["driver"]:
            log.critical("Have driver for %s", r)
    return res_names


def map_devices(board):
    log.critical("MAP board devices")
    log.critical(board)
    board_instance = board["cls"]()
    print(get_resources(board_instance))
