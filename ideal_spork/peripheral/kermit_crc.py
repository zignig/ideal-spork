# Lifted from 
# https://github.com/tpwrules/tasha_and_friends/blob/master/tastaf/gateware/uart.py#L246
# TODO  , covert to a Peripheral

from nmigen import *
from ..cores.periph import Peripheral, Register

class KermitCRC(Peripheral,Elaboratable):
    def __init__(self):
        super().__init__()
        bank = self.csr_bank()
        # reset engine and set CRC to 0
        self.reset = bank.csr(1,'w')
        # start CRC of the given byte. will give the wrong value if engine isn't
        # done yet!
        # the given byte
        self.byte = bank.csr(8,'w')
        # the crc value
        self.crc = bank.csr(16,'r')

    def elaborate(self, platform):
        m = Module()
        m.submodules.bridge = self._bridge

        bit_counter = Signal(range(9)) # count from 7 to 0
        crc = Signal(16)

        with m.If(self.reset.w_stb):
            m.d.sync += [
                bit_counter.eq(0),
                self.crc.eq(0),
            ]
        with m.Elif(self.byte.w_stb):
            m.d.sync += [
                bit_counter.eq(8),
                crc.eq(self.crc ^ self.byte.w_data)
            ]
        with m.Elif(bit_counter > 0):
            m.d.sync += [
                bit_counter.eq(bit_counter-1),
                crc.eq((crc >> 1) ^ Mux(crc[0], 0x8408, 0)),
            ]
        with m.Elif(bit_counter==0):
            m.d.sync += self.crc.r_data.eq(crc)
        return m
