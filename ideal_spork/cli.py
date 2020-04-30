# Command line interface.
import sys,os
import argparse 

description = "spork is a nmigen board build helper"
epilog = """
    ideal_spork is a nmigen_board builder\n

    spork init will create all the files for a platform build

    """

def as_options(parser):
    action = parser.add_subparsers(dest="action")
    action.add_parser("init",help="Create files for a  new board")
    action.add_parser("console",help="Attach to a new console")
    action.add_parser("list",help="List available firmware")
    action.add_parser("build",help="Build gateware and program onto the board")
    action.add_parser("program",help="Upload the give firmware onto the board")
    action.add_parser("gatesim",help="Run a gate simulation of the board")
    return parser

def as_main(args=None):
    if args is None:
        parser = argparse.ArgumentParser(description=description,epilog=epilog)
        args = as_options(parser).parse_args()
    if len(sys.argv)==1:
        # Check for the .spork file
        try:
            s = os.stat('.spork')
            print(s)
        except FileNotFoundError:
            parser.print_help(sys.stderr)
            sys.exit(1)

    if args.action == "init":
        from .boards import _select_board as b
        print(b.short_list())
        
