# Spork templated file
# Created on Thu May  7 17:10:44 2020

from nmigen import *
from nmigen_boards.alchitry_au import AlchitryAuPlatform

from blinky import Blinky


class alchitry_au(Elaboratable):
    def __init__(self, platform):
        # Add some resources
        platform.add_resources([])

    def elaborate(self, platform):
        m = Module()
        m.submodules.blinky = Blinky()
        return m


if __name__ == "__main__":
    platform = AlchitryAuPlatform()
    dut = alchitry_au(platform)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--program", action="store_true")
    parser.add_argument("-s", "--simulate", action="store_true")
    args = parser.parse_args()

    if args.simulate:
        from nmigen.cli import pysim

        with pysim.Simulator(dut, vcd_file=open("view_alchitry_au.vcd", "w")) as sim:
            sim.add_clock(1e-3)
            sim.run_until(1000, run_passive=True)

    if args.program:
        platform.build(dut, do_program=True)
