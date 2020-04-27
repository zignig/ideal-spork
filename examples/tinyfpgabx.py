" Example spork "

from nmigen import *
from ideal_spork.cpu.boneless import BonelessSpork

from ideal_spork.peripheral.serial import AsyncSerialPeripheral
from ideal_spork.peripheral.timer import TimerPeripheral
from ideal_spork.peripheral.leds import LedPeripheral

from nmigen_boards.tinyfpga_bx import TinyFPGABXPlatform
from nmigen_boards.resources.interface import UARTResource
from nmigen.build import Resource, Subsignal, Pins, Attrs

from boneless.arch.opcode import Instr
from boneless.arch.opcode import *

class TestSpork(Elaboratable):
    def __init__(self, platform, mem_size=32,firmware=None):
        self.cpu = cpu = BonelessSpork(firmware=firmware,mem_size=mem_size)

        uart = platform.request("uart")
        uart_divisor = int(platform.default_clk_frequency // 115200)

        serial = AsyncSerialPeripheral(pins=uart, divisor=uart_divisor)
        cpu.add_peripheral(serial)

        timer = TimerPeripheral(16)
        cpu.add_peripheral(timer)

        led = platform.request("led")
        status_led = LedPeripheral(led)
        cpu.add_peripheral(status_led)

        # build the register map        
        cpu.build()

    def elaborate(self, platform):
        m = Module()
        m.submodules.cpu = self.cpu
        return m

def Firmware(reg):
    print(reg)
    return [
        MOVI(R0,1),
        STXA(R0,reg.status_led_en),
        STXA(R0,reg.timer_en),
        STXA(R0,reg.timer_ev_enable),
        MOVI(R0,0xF),
        STXA(R0,reg.timer_reload),
        L("LOOP"),
        MOVI(R0,0),
        STXA(R0,reg.status_led_led),
        MOVI(R0,1),
        STXA(R0,reg.status_led_led),
        J("LOOP")
    ]
    
if __name__ == "__main__":
    print("Testing Spork")
    platform = TinyFPGABXPlatform()
    # FTDI on the tinybx
    platform.add_resources(
        [
            UARTResource(
                0, rx="A8", tx="B8", attrs=Attrs(IO_STANDARD="SB_LVCMOS", PULLUP=1)
            )
        ]
    )
    spork = TestSpork(platform)

    f = Firmware(spork.cpu.map)
    spork.cpu.firmware(f)

    from nmigen.cli import pysim
    with pysim.Simulator(spork, vcd_file=open("view_spork.vcd", "w")) as sim:
        sim.add_clock(10)
        #sim.add_sync_process(sim_data(test_string, mo.sink, mo.source))
        sim.run_until(5000, run_passive=True)
    #platform.build(spork)
