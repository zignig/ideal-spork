
from . import Construct

__all__ = ["Empty"]


class Empty(Construct):
    " Empty board with nothing "

    def __init__(self):
        super().__init__()
        self.files = {"empty/board.py.tmpl": None}
