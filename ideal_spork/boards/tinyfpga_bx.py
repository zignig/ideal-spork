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
        log.critical("unbuilt")
        self.usb = "1209:2100"
