# Board builder

from .select_board import interactive, show_list, check_board

from ..logger import logger

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
        files = ["blinky", "base"]


class Boneless(Construct):
    pass


class BoardBuilder:
    " Builds boards based on answers"

    def __init__(self, board=None, force=False, interactive=False, construct=Blinky):
        log.critical("Activate the board builder")
        self._built = False
        self.board = board
        self.force = force
        self.interactive = interactive
        self.construct = construct

    def build(self):
        log.critical("Build a board")
        selected_board = None
        if self.interactive:
            interactive(self.board)
        else:
            if self.board is None:
                show_list()
                print("use spork init -b <board name> to select a board")
            else:
                selected_board = check_board(self.board)
                if selected_board == None:
                    return
        log.critical(selected_board)
