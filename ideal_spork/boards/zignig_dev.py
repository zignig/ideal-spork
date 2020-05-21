# builder questions for spork
# my dev board.

from tinyfpga_bx import TinyFPGABXPlatform

from ..logger import logger

log = logger(__name__)


class zignig_dev(TinyFPGABXPlatform):
    comment = """
    
    This is a bread boarded tinybx , with some leds and an FTDI  
    
    """

    def __init__(self):
        super().__init__(self)
        self.usb = "0403:6001"
        log.critical("unbuilt")
