from boneless.arch.opcode import Instr
from boneless.arch.opcode import *

from ideal_spork.firmware.base import *

# Subroutine
class EchoChar(SubR):
    def instr(self):
        reg = self.reg
        return [
            # load the rx data
            LDXA(R3, reg.serial.rx.data),
            # send the byte to the crc engine
            STXA(R3, reg.crc.byte),
            # send the byte back out on the TX
            STXA(R3, reg.serial.tx.data),
        ]


# inline function
def Blink(w, reg):
    return [
        LDXA(w.temp, reg.timer.ev.pending),
        CMPI(w.temp, 1),
        # it has expired blink
        BNE("skip_blink"),
        MOVI(w.temp, 1),
        STXA(w.temp, reg.timer.ev.pending),
        # invert
        # write back to the leds
        STXA(w.leds, reg.status.led),
        XORI(w.leds, w.leds, 0xFFFF),
        L("skip_blink"),
    ]


def Init(w, reg):
    return [
        MOVI(w.temp, 1),
        STXA(w.temp, reg.status.en),
        # STXA(w.temp, reg.status_led_led),
        # load the timer
        MOVI(w.temp, 0xFFFF),
        STXA(w.temp, reg.timer.reload_0),
        MOVI(w.temp, 0x00FF),
        STXA(w.temp, reg.timer.reload_1),
        # enable timer and events
        MOVI(w.temp, 1),
        STXA(w.temp, reg.timer.en),
        STXA(w.temp, reg.timer.ev.enable),
        # reset the crc
        MOVI(w.temp, 1),
        STXA(w.temp, reg.crc.reset),
    ]


class Echo(Firmware):
    def setup(self):
        self.w.req(["leds", "temp"])

    def instr(self):
        echo_char = EchoChar()
        reg = self.reg
        w = self.w
        return [
            Init(w, reg),
            L("main_loop"),
            Blink(w, reg),
            # is there a char on the uart ?
            LDXA(w.temp, reg.serial.rx.rdy),
            CMPI(w.temp, 1),
            BNE("skip_echo"),
            echo_char(),
            L("skip_echo"),
            J("main_loop"),
        ]
