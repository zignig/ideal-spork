# Board builder

from .select_board import interactive, show_list, check_board
from .construct import choose_construct, interactive_construct
from ..logger import logger
from .map_board import map_devices

log = logger(__name__)

# 1. Select Board
# 2. Select Construct
# 3. Based on construct build peripherals
# 4. Use ideal_spork imports or copy locally ( as a question )
# 5. build and deploy


class Construct:
    pass


class Blinky(Construct):
    def __init__(self):
        files = ["/blinky/base.py.tmpl", "base"]


class Boneless(Construct):
    pass


class Sequencer(Construct):
    pass


available = [Blinky, Boneless, Sequencer]


class BoardBuilder:
    " Builds boards based on answers"

    def __init__(self, board=None, force=False, interactive=False, construct="Blinky"):
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
                print('Use "spork init -b <board name>" to select a board\n')
            else:
                self.board = check_board(self.board)
                if self.board == None:
                    return
        log.info("Select a construct")
        if self.interactive:
            self.construct = interactive_construct(available, self.construct)
        self.construct = choose_construct(available, self.construct, self.board)

        log.critical("Selected Board %s", self.board)
        log.critical("Selected Construct %s", self.construct)
        # At this point we have checked boards and constructs
        devices = map_devices(self.board)
