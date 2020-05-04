from nmigen import *

from ..cores.periph import Peripheral, Register

from ..cores.warmboot import warmboot

from ..logger import logger

log = logger(__name__)


@Register(platform="ice40")
class WarmBoot(Peripheral, Elaboratable):
    def __init__(self):
        log.info("Create Warmboot Peripheral")
        super().__init__()
        bank = self.csr_bank()
        self._image = bank.csr(2, "w")
        self._en = bank.csr(1, "w")
        # expose in object so the external can be connected
        self.warm = warmboot()

    def elaborate(self, platform):
        m = Module()
        m.submodules.bridge = self._bridge
        m.submodules.warm = warm = self.warm
        # bind the signals
        m.d.sync += [warm.image.eq(self._image.w_data), warm.boot.eq(self._en.w_data)]
        return m
