
from . import Construct


class CSR(Construct):
    " Just a CSR interface for all available drivers (UNFINISHED)"

    def __init__(self):
        super().__init__()
        log.critical("No CSR construct yet")
        self.files = {}
