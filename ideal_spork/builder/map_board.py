# Maps devices and peripherals to a board
from ..logger import logger

log = logger(__name__)

from ..peripheral import *
from ..utils import search


def _res_for_board(board_instance):
    return


def get_resources(board_instance):
    " Cross check drivers on the given board"
    res = list(board_instance.resources.keys())
    res_names = set()
    for i in res:
        res_names.add(i[0])
    log.debug(search.catalog.sections)
    for r in res_names:
        if r in search.catalog.sections["driver"]:
            log.warning("Have driver for %s", r)
    log.warning(res_names)
    residual = None
    return res_names, residual


def check_clock(board_instance):
    " Check if the default clock is < 22Mhz, if not divide"
    log.critical(board_instance)
    log.critical("Clock check Unfinshed")
    clock = None
    res = list(board_instance.resources.keys())
    for resource in res:
        if resource.startswith("clk"):
            log.critical("Clock %s", str(esource))
    return clock


def map_devices(board):
    " Convert a board type into drivers and clocks"
    log.info("MAP board devices")
    board_instance = board["cls"]()
    devices, residual = get_resources(board_instance)
    clock = check_clock(board_instance)
    return clock, devices, residual
