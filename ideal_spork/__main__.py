" Module level main"
from .logger import logger

log = logger(__name__)

from .builder.select_board import extract_boards, board_info, get_board
from .builder.file_gen import FileBuilder
from .builder.map_board import map_devices
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
        try:
            devices = map_devices(bi)
            fb = FileBuilder(
                devices=devices, board=bi, construct=BoardOnly, name=i, force=args.force
            )
            fb.build()
        except BaseException as b:
            log.error("{:s}".format(i))
            log.error("\t{:s}".format(str(b)))
