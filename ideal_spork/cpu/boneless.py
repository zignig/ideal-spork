"""
Base boneless object
"""
from nmigen import *

from boneless.gateware.core import CoreFSM
from boneless.gateware.alsru import ALSRU_4LUT

from ..cores.periph.bus import PeripheralCollection

class BonelessSpork(Elaboratable):
    def __init__(self,firmware=None,mem_size=512):
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

    def add_peripheral(self,periph):
        self.pc.add(periph)

    def elaborate(self,platform):
        m = Module()
        # attach the cpu and bus
        m.submodules.cpu = self.cpu        
        m.submodules.bus = self.bus
        
        # connect the bus to the cpu
        m.d.comb += [
            self.bus.addr.eq(self.cpu.o_bus_addr),
        ]
        return m
