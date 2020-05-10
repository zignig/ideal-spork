# Command line interface.
import sys, os
import argparse

import logging
from .logger import logger, set_logging_level

log = logger(__name__)

from .utils.spork_file import load_spork

description = "spork is a nmigen board build helper"
epilog = """\
        You probably want "spork init <project name> -i" \n\n
    """


class SporkError(Exception):
    pass


def as_options(parser):
    action = parser.add_subparsers(dest="action")

    # Create a new SPORK
    init_action = action.add_parser("init", help="Create files for a  new board")
    init_action.add_argument("-b", "--board", help="Specify the board to generate")
    init_action.add_argument(
        "ProjectName",
        default="MySpork",
        help="Specify the name of the class to generate",
    )
    init_action.add_argument(
        "-c", "--construct", help="Select a construct", default=None
    )
    init_action.add_argument(
        "-f", "--force", help="Force board creation", action="store_true"
    )
    init_action.add_argument(
        "-i", "--interactive", help="Interactive board creation", action="store_true"
    )
    init_action.add_argument(
        "--local",
        help="Create local files, does not need ideal_spork to run",
        action="store_true",
    )

    # Unbound
    action.add_parser("info", help="Get information from the base board")
    action.add_parser("console", help="Attach to a new console (UMFINISHED)")
    action.add_parser(
        "build", help="Build gateware and program onto the board (UNFINISHED)"
    )
    action.add_parser("status", help="Get the status of the current spork (UNFINISHED)")
    action.add_parser("update", help="Update all the fixed assets (UNFINISHED)")

    # List boards and active peripherals
    action.add_parser("list", help="List available boards")

    # add firmware to build image
    init_burn = action.add_parser("burn", help="Add the given firmware to boot image")
    init_burn.add_argument(
        "program", default=None, help="Specify the firmware to upload"
    )
    init_burn.add_argument(
        "--no-bootloader", help="Do not include the bootloadeor in the image"
    )

    # Push a firmware
    init_program = action.add_parser(
        "program", help="Upload the given firmware onto the board"
    )
    init_program.add_argument("program", help="Specify the firmware to upload")

    # Simulate TODO convert to compiled sim
    action.add_parser("gatesim", help="Run a gate simulation of the board")

    # Developer tools

    from .developer import developer_tooling

    developer_tooling(action)

    return parser


def as_main(args=None):
    if args is None:
        parser = argparse.ArgumentParser(description=description, epilog=epilog)
        parser.add_argument("-v", help="Warn Logging Level", action="store_true")
        parser.add_argument("-vv", help="Info Logging Level", action="store_true")
        parser.add_argument("-vvv", help="Debug Logging Level", action="store_true")
        # Unfinished
        parser.add_argument(
            "-d", "--directory", help="Directory for spork file", default="."
        )
        args = as_options(parser).parse_args()

    # Turn on verbosity
    if args.v:
        set_logging_level(logging.WARNING)
    if args.vv:
        set_logging_level(logging.INFO)
    if args.vvv:
        set_logging_level(logging.DEBUG)

    # Check for the .spork file
    the_spork = None
    try:
        # TODO use directory for this file
        s = os.stat(".spork")
        log.debug("spork file exists")
        the_spork = load_spork(".spork")
    except FileNotFoundError:
        log.critical("Spork file missing")
        log.critical("Please template the .spork file")
        log.critical("Check for .fork file")
        print("No spork file")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.action == "init":
        from .builder.create import BoardBuilder

        bb = BoardBuilder(
            board=args.board,
            force=args.force,
            interactive=args.interactive,
            construct=args.construct,
            name=args.ProjectName,
            local=args.local,
        )
        bb.build()

    if args.action == "info":
        if the_spork is not None:
            the_spork.show()
        else:
            log.critical(".spork file does not exist")
            raise SporkError("Spork info UNFINISHED")

    if args.action == "console":
        from .host.console import Console

        console = Console(the_spork)
        log.critical("Only does echo test of datetime, for now")
        console.attach()

    if args.action == "burn":
        # Add the firmware onto the boot system
        raise SporkError("UNFINISHED - Burn not working yet")

    if args.action == "status":
        raise SporkError("UNFINISHED  - Status not working yet, get board status")

    if args.action == "list":
        from .builder.select_board import short_list

        print(" Available Boards ")
        print()
        for num, board in enumerate(short_list()):
            print("{:>4}  {}".format(num, board))
        print()

    if args.action == "build":
        raise SporkError("UNFINISHED - Build unfinished: make gateware and upload")

    if args.action == "program":
        if args.program == None:
            if hasattr(the_spork, "firmware"):
                print(the_spork.firmware)
            else:
                raise SporkError(
                    "No default firmware use -p to specify or add 'firmware: <name>' to the .spork file"
                )
        else:
            log.critical("UNFINISHED - Run this program, unfinished")

        raise SporkError("Program Unfinished")

    if args.action == "gatesim":
        raise SporkError("UNFINISHED - gatesim in pysim or ctxxx")
