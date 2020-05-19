# builder questions for spork

from ..logger import logger
from tinyfpga_bx import TinyFPGABXPlatform

log = logger(__name__)


class zignig_dev(TinyFPGABXPlatform):
    comment = """
    
    This is a bread boarded tinybx , with some leds and an FTDI  
    
    """

    def __init__(self):
        log.critical("unbuilt")
        self.usb = "0403:6001"
