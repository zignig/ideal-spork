# Maps devices and peripherals to a board
from ..logger import logger

log = logger(__name__)

from ..peripheral import *
from ..utils import search


def _res_for_board(board_instance):
    res = list(board_instance.resources.keys())
    res_names = set()
    for i in res:
        res_names.add(i[0])
    return res_names


def get_resources(board_instance):
    " Cross check drivers on the given board"
    res_names = _res_for_board(board_instance)
    log.debug(search.catalog.sections)
    for res in res_names:
        if res in search.catalog.sections["driver"]:
            log.warning("Have driver for %s", res)
    log.warning(res_names)
    residual = None
    return res_names, residual


def check_clock(board_instance):
    " Check if the default clock is < 22Mhz, if not divide"
    log.critical(board_instance)
    log.critical("Clock check Unfinshed")
    clock = None
    res_names = _res_for_board(board_instance)
    for res in res_names:
        if res.startswith("clk"):
            log.critical("Clock %s", str(res))
    return clock


def map_devices(board):
    " Convert a board type into drivers and clocks"
    log.info("Map board devices for %s", board)
    board_instance = board["cls"]()
    devices, residual = get_resources(board_instance)
    clock = check_clock(board_instance)
    return clock, devices, residual
