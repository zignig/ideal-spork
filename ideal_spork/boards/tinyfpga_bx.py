# builder questions for spork

from ..logger import logger

log = logger(__name__)


class TinyFPGABXPlatform:
    comment = """
    
    The tinybx only has a usb interface and one led.

    nmigen does not have a pure gateware usb interface yet...
    have a look at https://github.com/lambdaconcept/lambdaUSB , the phy needs some work.

    Use an FTDI on some pins
    
    """

    def __init__(self):
        self.usb = "1209:2100"
        self.flash_map = {
            "bootloader": (0x000a0, 0x28000),
            "userimage": (0x28000, 0x50000),
            "userdata": (0x50000 - 0x100000),
        }
        log.critical("(unfinished)")
