" A button builder "
# IRC reference

# reference https://paste.debian.net/1145089/
# see https://freenode.irclog.whitequark.org/nmigen/2020-05-05#26964009


# btn_i = Signal()
# m.submodules += FFSynchronizer(platform.request("btn"), btn)
#
# btn_r = Signal()
# btn_o = Signal()
# timer = Signal(range(1024), reset=1023)
# with m.If(btn_i != btn_r):
#    m.d.sync += btn_r.eq(btn_i)
#    m.d.sync += timer.eq(timer.reset)
# with m.Elif(timer != 0):
#    m.d.sync += timer.eq(timer - 1)
# with m.Else():
#    m.d.sync += btn_o.eq(btn_i)

__working__ = False

from nmigen import *

from ..cores.periph.base import Peripheral
from ..utils.search import Enroll

from ..logger import logger

log = logger(__name__)

__all__ = ["ButtonPeripheral"]


@Enroll(driver="button")
class ButtonPeripheral(Peripheral, Elaboratable):
    def __init__(self):
        log.info("Create Button Peripheral")
        super().__init__()
        bank = self.csr_bank()
        self._en = bank.csr(1, "w")
        self._button = bank.csr(16, "w")

    def elaborate(self, platform):
        m = Module()
        # Code here
        return m
