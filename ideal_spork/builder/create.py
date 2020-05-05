# Board builder

from .select_board import interactive, show_list, check_board
from .construct import choose_construct, interactive_construct
from ..logger import logger
from .map_board import map_devices
from .interactive import select_from_list

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

    pass


class Sequencer(Construct):
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
        log.debug("Build a board")
        log.info("Select a board")
        if self.interactive:
            interactive(self.board)
        else:
            if self.board is None:
                show_list()
                print('Use "spork init -b <board name>" to select a board')
                print("or... spork init -i for console questions\n")
            else:
                self.board = check_board(self.board)
                if self.board == None:
                    return

        log.info("Select a construct")
        if self.interactive:
            self.construct = interactive_construct(available, self.construct)
        else:
            self.construct = choose_construct(available, self.construct, self.board)

        log.warning("Selected Board %s", self.board)
        log.warning("Selected Construct %s", self.construct)

        # At this point we have checked boards and constructs

        devices = map_devices(self.board)
