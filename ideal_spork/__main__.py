" Module level main"
from .logger import logger

log = logger(__name__)

from .builder.select_board import extract_boards, board_info, get_board
from .builder.file_gen import FileBuilder
from .builder.create import *

print("Ideal Spork")
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dumpall", help="generate Empty for all boards", action="store_true"
)
parser.add_argument("--force", help="force overwrite", action="store_true")
args = parser.parse_args()

if args.dumpall:
    full_list = extract_boards()
    for i in full_list:
        bi = board_info(get_board(i))
        print(bi)
        fb = FileBuilder(board=bi, construct=BoardOnly, name=i, force=args.force)
        fb.generate()
