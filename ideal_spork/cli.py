# Command line interface.
import sys,os
import argparse 

description = "spork is a nmigen board build helper"
epilog = "Build a board"

def as_options(parser):
    action = parser.add_subparsers(dest="action")
    action.add_parser("new",help="Create a new board")
    action.add_parser("console",help="Attach to a new console")
    action.add_parser("list",help="List available firmware")
    action.add_parser("build",help="Build gateware and program onto the board")
    action.add_parser("program",help="Upload the give firmware onto the board")
    action.add_parser("gatesim",help="Run a gatesimulation of the board")
    return parser

def as_main(args=None):
    if args is None:
        args = as_options(argparse.ArgumentParser(description=description,epilog=epilog)).parse_args()
    #input  = args.input.read()
    #output = args.output or sys.stdout
    print(args.action)
    if args.action == "info":
        print('Do info')
