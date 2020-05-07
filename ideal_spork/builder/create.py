# Board builder

from .select_board import select_board, show_list, check_board
from .construct import check_construct, interactive_construct
from .map_board import map_devices
from .interactive import select_from_list
from .file_gen import FileBuilder

from ..logger import logger

log = logger(__name__)

__all__ = ["Empty", "Blinky", "CSR", "Boneless", "Sequencer", "BoardOnly"]

# 1. Select Board
# 2. Select Construct
# 3. Based on construct build peripherals
# TODO 4. Use ideal_spork imports or copy locally ( as a question )
# TODO 5. build and deploy


class Construct:
    pass


class Empty(Construct):
    " Empty board with nothing "

    def __init__(self):
        self.files = {"empty/board.py.tmpl": None}


class BoardOnly(Construct):
    " Just subclass the board "

    def __init__(self):
        self.files = {"board_only/board.py.tmpl": None}


class Blinky(Construct):
    " Blink with switch and button invert "

    def __init__(self):
        self.files = {
            "blinky/blinky.py.tmpl": "blinky.py",
            "blinky/board.py.tmpl": None,
        }


class CSR(Construct):
    " Just a CSR interface for all available drivers (UNFINISHED)"

    def __init__(self):
        log.critical("No CSR construct yet")
        self.files = {}


class Boneless(Construct):
    " Boneless processor with peripherals (IN PROGRESS)"

    def __init__(self):
        self.files = {
            "boneless/firmware.py.tmpl": "firmware.py",
            "boneless/board.py.tmpl": None,
        }
        self.peripheral = ["TimerPeripheral"]


class Sequencer(Construct):
    " Base command sequencer (UNFINISHED)"

    def __init__(self):
        log.critical("No Sequencer construct yet")
        self.files = []


available = [Empty, BoardOnly, Blinky, Boneless, Sequencer, CSR]


class BoardBuilder:
    " Builds boards based on answers and questions "
    prolog = "Spork V0.1a"

    def __init__(
        self,
        board=None,
        force=False,
        interactive=False,
        construct=None,
        name="TheSPORK",
    ):
        log.debug("Activate the board builder")
        self._built = False
        self.board = board
        self.force = force
        self.interactive = interactive
        self.construct = construct
        self.name = name

    def build(self):
        log.info("Select a board")
        print(self.prolog)
        if self.interactive and (self.board is None):
            self.board = select_board()
            log.info("Interactive answer %s", self.board)
        else:
            self.board = check_board(self.board)
            if self.board is None:
                print('Use "spork init -b <board name>" to select a board')
                print("or... spork init -i for console questions\n")
                return

        log.info("Select a construct")
        if self.interactive and (self.construct is None):
            self.construct = interactive_construct(available, self.construct)
        else:
            self.construct = check_construct(available, self.construct)
            if self.construct is None:
                print('Use "spork init -c <construct>" to select a construct')
                print("or... spork init -i for console questions\n")
                return

        log.info("Selected Board %s", self.board["class_name"])
        log.info("Selected Construct %s", self.construct)

        # At this point we have checked boards and constructs

        log.info("Map all the IO")
        devices = map_devices(self.board)

        log.critical("Check registered boards")
        # TODO

        log.info("Template the files")
        builder = FileBuilder(
            name=self.name,
            board=self.board,
            construct=self.construct,
            devices=devices,
            force=self.force,
        )
        builder.build()  # TODO add directory target
