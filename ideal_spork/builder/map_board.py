# Maps devices and peripherals to a board
from ..logger import logger

log = logger(__name__)

from ..peripheral import *
from ..utils import search

# TODO the return data is not well formed


class BoardError(Exception):
    pass


class BoardInfo:
    " Class to hold all the board information "
    # this construct is useful.
    def __init__(self):
        object.__setattr__(self, "sections", [])

    def __setattr__(self, name, value):
        log.debug("{:s} {:s}".format(str(name), str(value)))
        if hasattr(self, name):
            raise BoardError("Board section {:s} already exists".format(name))
        object.__setattr__(self, name, value)
        self.sections.append(name)

    def as_dict(self):
        the_dict = {}
        for i in self.sections:
            log.debug("{:s} : {:s}".format(str(i), str(self.sections[i])))
            the_dict[i] = getattr(self, i)
        return the_dict


def _res_for_board(board_instance):
    " Get a list of all the resources of a board "
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
    log.warning("Clock check Unfinshed")
    clock = []
    if hasattr(board_instance, "default_clk_frequency"):
        default_freq = board_instance.default_clk_frequency
        if default_freq > 22e6:
            in_Mhz = int(default_freq / 1e6)
            log.warning(
                "{:s} clock too fast at {:s} Mhz.".format(
                    str(board_instance.__module__), str(in_Mhz)
                )
            )
            res_names = _res_for_board(board_instance)
            for res in res_names:
                if res.startswith("clk"):
                    log.debug("Clock %s", str(res))
                    clock.append(res)
    else:
        log.info("Board does not have exteral clock")
    return clock


def map_connectors(board_instance):
    log.info("Find the connectors and IO")
    conn = board_instance.connectors
    for c in conn:
        log.info("{:s} - {:s}".format(str(c), str(conn[c])))
    return conn


def map_devices(board):
    " Convert a board type into drivers, io  and clocks"
    log.info("Map board devices for %s", board["class_name"])
    # Make an instance of the board
    board_instance = board["cls"]()
    log.debug("Find drivers for the given board")
    peripherals, residual = get_resources(board_instance)
    log.debug("Check the clock settings")
    clock = None  # check_clock(board_instance)
    log.debug("Map connectors and IO")
    io = map_connectors(board_instance)
    log.debug("Build the info block")
    bi = BoardInfo()
    bi.clock = clock
    bi.peripherals = peripherals
    bi.residual = residual
    bi.io = io
    return bi
