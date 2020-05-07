# Maps devices and peripherals to a board
from ..logger import logger

log = logger(__name__)

from ..peripheral import *
from ..utils import search

# TODO the return data is not well formed


def _res_for_board(board_instance):
    res = list(board_instance.resources.keys())
    res_names = set()
    for i in res:
        res_names.add(i[0])
    return res_names


def get_resources(board_instance):
    " Cross check drivers on the given board"
    res_names = _res_for_board(board_instance)
    residual = _res_for_board(board_instance)
    log.debug(search.catalog.sections)
    drivers = []
    driver_list = search.catalog.sections["driver"]
    for res in res_names:
        log.debug("Resource {:s}".format(res))
        if res in driver_list:
            log.info("Have driver for %s", res)
            drivers.append((res, driver_list[res]))
            residual.remove(res)
    return (drivers, residual)


def check_clock(board_instance):
    " Check if the default clock is < 22Mhz, if not divide"
    default_freq = board_instance.default_clk_frequency
    if default_freq > 22e6:
        log.warning("Clock at %s is to fast need too divide", default_freq)
    log.warning("Clock check Unfinshed")
    clock = None
    res_names = _res_for_board(board_instance)
    for res in res_names:
        if res.startswith("clk"):
            log.debug("Clock %s", str(res))
            clock = res
    return clock


def map_connectors(board_instance):
    log.debug("Find the connectors and IO")
    conn = board_instance.connectors
    for c in conn:
        log.info("{:s} - {:s}".format(str(c), str(conn[c])))
    return conn


def map_devices(board):
    " Convert a board type into drivers, io  and clocks"
    log.info("Map board devices for %s", board["class_name"])
    board_instance = board["cls"]()
    log.debug("Find drivers for the given board")
    peripherals, residual = get_resources(board_instance)
    log.debug("Check the clock settings")
    clock = check_clock(board_instance)
    log.debug("Map connectors and IO")
    io = map_connectors(board_instance)
    # TODO , this is a bit janky
    o = type(
        "device",
        (object,),
        dict(clock=clock, peripherals=peripherals, residual=residual, io=io),
    )
    return o
