" Example spork " 

from nmigen import * 
from ideal_spork.cpu.boneless import BonelessSpork
from ideal_spork.peripheral.serial  import  AsyncSerialPeripheral

from nmigen_boards.tinyfpga_bx import TinyFPGABXPlatform
from nmigen_boards.resources.interface import UARTResource
from nmigen.build import Resource, Subsignal, Pins, Attrs

class TestSpork(Elaboratable):
    def __init__(self,platform,mem_size=512):
        self.cpu = cpu = BonelessSpork()
        
        uart = platform.request('uart')
        uart_divisor = int(platform.default_clk_frequency // 115200 )

        serial = AsyncSerialPeripheral(pins=uart,divisor=uart_divisor)
        cpu.add_peripheral(serial)
 
    def elaborate(self,platform):
        m = Module()
        m.submodules.cpu = self.cpu
        return m
        

if __name__ == "__main__":
    print("Testing Spork")
    platform = TinyFPGABXPlatform()
    # FTDI on the tinybx
    platform.add_resources([
        UARTResource(
            0, rx="A8", tx="B8", attrs=Attrs(IO_STANDARD="SB_LVCMOS", PULLUP=1)
        ),
    ])    
    spork = TestSpork(platform)
    platform.build(spork)
