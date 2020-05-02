# Interactive Console

from ..logger import logger

log = logger(__name__)

import serial

# refer to https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html


class Console:
    def __init__(self, spork, timeout=0.5):
        log.info("Create console")
        log.critical("Unfinished")
        self.spork = spork
        self.serial_port = spork.serial_port
        self.serial_speed = spork.serial_speed
        self.timeout = timeout

    def attach(self):
        log.info("Serial port: %s", self.serial_port)
        log.info("Serial speed: %s", self.serial_speed)
        try:
            port = serial.Serial(
                self.serial_port, self.serial_speed, timeout=self.timeout
            )
        except:
            log.critical("Serial port %s does not exist", self.serial_port)
            return
        with port as p:
            while True:
                p.write("testing".encode("utf-8"))
                v = p.read(20)
                print(v)
        # console loop
