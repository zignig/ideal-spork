# Interactive Console

from ..logger import logger

log = logger(__name__)

import serial
import time

# refer to https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html


class Console:
    def __init__(self, spork, timeout=0.02):
        log.debug("Create console")
        self.spork = spork
        self.serial_port = spork.serial_port
        self.serial_speed = spork.serial_speed
        self.timeout = timeout

    def attach(self):
        log.debug("Serial port: %s", self.serial_port)
        log.debug("Serial speed: %s", self.serial_speed)
        try:
            port = serial.Serial(
                self.serial_port, self.serial_speed, timeout=self.timeout
            )
        except:
            log.critical("Serial port %s does not exist", self.serial_port)
            return
        log.critical("Unfinished")
        with port as p:
            while True:
                time_string = time.ctime()
                print("out->" + time_string + "<-")
                p.write(time_string.encode("utf-8"))
                v = p.read(1000)
                print("in ->" + v.decode("utf-8") + "<-")
                if v.decode("utf-8") != time_string:
                    log.critical("No response")
                    return
        # console loop
