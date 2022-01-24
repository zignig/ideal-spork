from . import Construct


class BoardOnly(Construct):
    " Just subclass the board "

    def __init__(self):
        super().__init__()
        self.files = {"board_only/board.py.tmpl": None}
