# Spork templated file
# Created on Thu May  7 17:10:44 2020

from nmigen import *
from nmigen_boards.versa_ecp5 import VersaECP5Platform

from blinky import Blinky


class versa_ecp5(Elaboratable):
    def __init__(self, platform):
        # Add some resources
        platform.add_resources([])

    def elaborate(self, platform):
        m = Module()
        m.submodules.blinky = Blinky()
        return m


if __name__ == "__main__":
    platform = VersaECP5Platform()
    dut = versa_ecp5(platform)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--program", action="store_true")
    parser.add_argument("-s", "--simulate", action="store_true")
    args = parser.parse_args()

    if args.simulate:
        from nmigen.cli import pysim

        with pysim.Simulator(dut, vcd_file=open("view_versa_ecp5.vcd", "w")) as sim:
            sim.add_clock(1e-3)
            sim.run_until(1000, run_passive=True)

    if args.program:
        platform.build(dut, do_program=True)
