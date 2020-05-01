# Command line interface.
import sys, os
import argparse

import logging
from .logger import logger
from .utils.spork_file import load_spork

log = logger(__name__)

description = "spork is a nmigen board build helper"
epilog = """
    ideal_spork is a nmigen_board builder\n

    spork init will create all the files for a platform build

    """


class SporkError(Exception):
    pass


def as_options(parser):
    action = parser.add_subparsers(dest="action")

    # Create a new SPORK
    init_action = action.add_parser("init", help="Create files for a  new board")
    init_action.add_argument("-b", "--board", help="Specify the board to generate")
    init_action.add_argument("-f", "--force", help="Force board creation")

    # Unbound
    action.add_parser("info", help="Get information from the base board")
    action.add_parser("console", help="Attach to a new console")
    action.add_parser("build", help="Build gateware and program onto the board")

    # List boards and active peripherals
    action.add_parser("list", help="List available boards")

    # add firmware to build image
    init_burn = action.add_parser("burn", help="Add the given firmware to boot image")
    init_burn.add_argument("program", help="Specify the firmware to upload")

    # Push a firmware
    init_program = action.add_parser(
        "program", help="Upload the given firmware onto the board"
    )
    init_program.add_argument("program", help="Specify the firmware to upload")

    # Simulate TODO convert to compiled sim
    action.add_parser("gatesim", help="Run a gate simulation of the board")
    return parser


def as_main(args=None):
    if args is None:
        parser = argparse.ArgumentParser(description=description, epilog=epilog)
        parser.add_argument(
            "-v", "--verbose", help="Logging Level", action="store_true"
        )
        args = as_options(parser).parse_args()

    # Turn on verbosity
    if args.verbose:
        log.setLevel(logging.DEBUG)

    # Check for the .spork file
    try:
        s = os.stat(".spork")
        log.debug("spork file exists")
        the_spork = load_spork(".spork")
    except FileNotFoundError:
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

    if args.action == "init":
        from .boards._select_board import interactive, check_board

        if args.board:
            check_board(args.board)
        else:
            interactive()

    if args.action == "info":
        raise SporkError()

    if args.action == "console":
        print(the_spork)
        raise SporkError()

    if args.action == "list":
        raise SporkError()

    if args.action == "build":
        raise SporkError()

    if args.action == "program":
        raise SporkError()

    if args.action == "gatesim":
        raise SporkError()
