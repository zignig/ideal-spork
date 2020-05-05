# Board builder

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
    pass


class Boneless(Construct):
    pass


class BoardBuilder:
    " Builds boards based on answers"

    def __init__(self, board=None, force=False, interactive=False, construct=Blinky):
        log.critical("Activate the board builder")
        self._built = False

    def build(self):
        log.critical("Build a board")
