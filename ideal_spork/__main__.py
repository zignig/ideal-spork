" Module level main"

import sys, traceback

from .logger import logger, set_logging_level
import logging

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
parser.add_argument("-f", "--force", help="force overwrite", action="store_true")
parser.add_argument("-v", help="Warn Logging Level", action="store_true")
parser.add_argument("-vv", help="Info Logging Level", action="store_true")
parser.add_argument("-vvv", help="Debug Logging Level", action="store_true")

args = parser.parse_args()

# show help if nothing
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

# Turn on verbosity
if args.v:
    set_logging_level(logging.WARNING)
if args.vv:
    set_logging_level(logging.INFO)
if args.vvv:
    set_logging_level(logging.DEBUG)

if args.dumpall:
    full_list = extract_boards()
    for i in full_list:
        bi = board_info(get_board(i))
        try:
            devices = map_devices(bi)
            fb = FileBuilder(
                devices=devices, board=bi, construct=Blinky, name=i, force=args.force
            )
            fb.build()
        except BaseException as b:
            log.error("{:s}".format(i))
            log.error("\t{:s}".format(str(b)))
            log.error("{:s}".format(str(traceback.print_exc())))
