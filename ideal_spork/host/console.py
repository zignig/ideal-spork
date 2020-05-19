# Interactive Console

from ..logger import logger

log = logger(__name__)

import serial
import time
import sys, tty, termios

# refer to https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html


class Console:
    def __init__(self, spork, timeout=0.5):  # timeout=0.02):
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
        except serial.serialutil.SerialException as e:
            log.error(e)
            return
        log.critical("Unfinished")
        return

    def command_line(self):
        # Define data-model for an input-string with a cursor
        input = ""
        index = 0
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        while True:  # loop for each character
            char = ord(sys.stdin.read(1))  # read one char and get char code
            if char == 3:
                break
            sys.stdout.write(chr(char))
            sys.stdout.flush()
        log.critical("Exit console")
        termios.tcsetattr(fd, termios.TCSAFLUSH, old_settings)
