# builder questions for spork

from ..logger import logger
from tinyfpga_bx import TinyFPGABXPlatform

log = logger(__name__)


class zignig_dev(TinyFPGABXPlatform):
    comment = """
    
    This is a bread boarded tinyby , with some leds and an FTDI  
    
    """

    def __init__(self):
        log.critical("unbuilt")
