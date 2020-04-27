"""
Base boneless object
"""
from nmigen import *

from boneless.gateware.core import CoreFSM
from boneless.gateware.alsru import ALSRU_4LUT
from boneless.arch.opcode import Instr
from boneless.arch.opcode import *

from ..cores.periph.bus import PeripheralCollection


class BuildException(Exception):
    pass


class BonelessSpork(Elaboratable):
    def __init__(self, firmware=None, mem_size=512):
        # create the memory
        self.mem_size = mem_size
        self.memory = Memory(width=16, depth=self.mem_size)
        # create the CPU core
        self.cpu = CoreFSM(
            alsru_cls=ALSRU_4LUT,
            memory=self.memory,
            reset_pc=0,
            reset_w=self.mem_size - 8,
        )
        # Create the peripheral bus
        self.pc = PeripheralCollection()
        self.bus = self.pc.bus._bus
        self.map = self.pc.map

        self._built = False

    def add_peripheral(self, periph):
        self.pc.add(periph)

    def build(self):
        if not self._built:
            # build the register map
            self.pc.build()
            self._build = True

    def firmware(self, fw=None):
        # compile and attach the firmware
        if fw is None:
            raise BuildException("No firmware")
        fw = Instr.assemble(fw)
        if len(fw) > self.mem_size - 8:
            raise BuildException("Firmware too long")
        self.memory.init = fw

    def elaborate(self, platform):

        self.build()
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
