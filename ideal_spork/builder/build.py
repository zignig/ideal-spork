# Board builder

from ..logger import logger

log = logger(__name__)

# 1. Select Board
# 2. Select Construct
# 3. Based on construct build peripherals
# 4. Use ideal_spork imports or copy locally ( as a question )
# 5. build and deploy


class BoardBuilder:
    " Builds boards based on answers"

    def __init__(self, board=None, construct=Blinky):
        self._built = False

    def build(self):
        log.critical("Build a board")