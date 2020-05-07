# Spork templated file
# Created on Thu May  7 11:53:23 2020
# Bare board
# home development tinybx

from nmigen import *
from nmigen_boards.tinyfpga_bx import TinyFPGABXPlatform

from nmigen_boards.resources.user import LEDResources, SwitchResources
from nmigen_boards.resources.interface import UARTResource
from nmigen.build import Resource, Subsignal, Pins, Attrs


class zignig_dev(TinyFPGABXPlatform):
    __sporked__ = True
    resources = TinyFPGABXPlatform.resources + [
        # FTDI link back to pc
        UARTResource(
            0, rx="A8", tx="B8", attrs=Attrs(IO_STANDARD="SB_LVCMOS", PULLUP=1)
        ),
        *LEDResources("led", pins="J1 H2 H9 D9", attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("reset_pin", 0, Pins("18", conn=("gpio", 0), dir="i")),
        #        *SwitchResources(pins="D10 D11", invert=True, attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
    ]
