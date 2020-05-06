# Board builder

from .select_board import select_board, show_list, check_board
from .construct import check_construct, interactive_construct
from .map_board import map_devices
from .interactive import select_from_list

from ..logger import logger

log = logger(__name__)

# 1. Select Board
# 2. Select Construct
# 3. Based on construct build peripherals
# 4. Use ideal_spork imports or copy locally ( as a question )
# 5. build and deploy


class Construct:
    pass


class Empty(Construct):
    " Empty board with nothing "
    pass


class Blinky(Construct):
    " Blink with switch and button invert "

    def __init__(self):
        files = ["/blinky/base.py.tmpl", "base"]


class CSR(Construct):
    " Just a CSR interface for all available drivers"
    pass


class Boneless(Construct):
    " Boneless processor with peripherals"
    pass


class Sequencer(Construct):
    " Base command sequencer (UNFINISHED)"
    pass


available = [Empty, Blinky, Boneless, Sequencer, CSR]


class BoardBuilder:
    " Builds boards based on answers and questions "

    def __init__(self, board=None, force=False, interactive=False, construct=None):
        log.debug("Activate the board builder")
        self._built = False
        self.board = board
        self.force = force
        self.interactive = interactive
        self.construct = construct

    def build(self):
        log.info("Select a board")
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

        log.critical("Selected Board %s", self.board)
        log.critical("Selected Construct %s", self.construct)

        # At this point we have checked boards and constructs

        devices = map_devices(self.board)
