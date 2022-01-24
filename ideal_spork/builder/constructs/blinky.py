from . import Construct


class Blinky(Construct):
    " Blink with switch and button invert "

    def __init__(self):
        super().__init__()
        self.files = {
            "blinky/blinky.py.tmpl": "blinky.py",
            "blinky/board.py.tmpl": None,
        }
