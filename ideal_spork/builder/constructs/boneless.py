
from . import Construct


class Boneless(Construct):
    " Boneless processor with peripherals (IN PROGRESS)"

    def __init__(self):
        super().__init__()
        self.files = {
            "boneless/firmware.py.tmpl": "firmware.py",
            "boneless/board.py.tmpl": None,
        }
        self.peripheral = ["TimerPeripheral"]
