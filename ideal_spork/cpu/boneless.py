"""
Base boneless object
"""
from nmigen import *

from boneless.gateware.core import CoreFSM
from boneless.gateware.alsru import ALSRU_4LUT

from ..cores.periph.bus import PeripheralCollection


class BonelessSpork(Elaboratable):
    def __init__(self, firmware=None, mem_size=512):
        # create the memory
        self.mem_size = mem_size
        self.memory = Memory(width=16, depth=self.mem_size)
        self.cpu = CoreFSM(
            alsru_cls=ALSRU_4LUT,
            memory=self.memory,
            reset_pc=0,
            reset_w=self.mem_size - 8,
        )
        self.pc = PeripheralCollection()
        self.bus = self.pc.bus._bus

    def add_peripheral(self, periph):
        self.pc.add(periph)

    def elaborate(self, platform):
        m = Module()

        # attach the cpu and bus
        m.submodules.cpu = self.cpu
        m.submodules.pc = self.pc

        # connect the bus to the cpu
        m.d.comb += [
            self.bus.addr.eq(self.cpu.o_bus_addr),
            self.bus.r_stb.eq(self.cpu.o_ext_re),
            self.bus.w_stb.eq(self.cpu.o_ext_we),
            self.bus.w_data.eq(self.cpu.o_ext_data),
            self.cpu.i_ext_data.eq(self.bus.r_data),
        ]
        return m
