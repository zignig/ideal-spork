from .base import *
import pprint
import math

from ..logger import logger

log = logger(__name__)
from boneless.arch.opcode import *
from boneless.arch.instr import Instr

from .stringer import Stringer


class Firmware:
    """ 
    Firmware construct 

    does initialization , main loop and library code
    """

    def __init__(self, reg=None, start_window=512):
        log.info("Create Firmware Object")
        self.w = Window()
        self.sw = start_window
        self.reg = reg

        # global string set
        self.stringer = st = Stringer()

        # attach the io_map to all the subroutines
        SubR.reg = self.reg
        Inline.reg = self.reg

        # attach global string to other
        SubR.stringer = self.stringer
        Inline.stringer = self.stringer
        # code objects
        self.obj = []
        self._built = False
        self.fw = None

    def setup(self):
        raise FWError("No setup function")

    def prelude(self):
        log.warning("No prelude(), use to setup code")
        return []

    def instr(self):
        return []

    def code(self):
        if not self._built:
            w = self.w = Window()
            ll = LocalLabels()
            self.setup()
            fw = [
                Rem("--- Firmware Object ---"),
                Rem(self.w._name),
                L("init"),
                MOVI(w.fp, self.sw - 8),
                STW(w.fp),
                self.prelude(),
                L("main"),
                self.instr(),
                J("main"),
                Rem("--- Library Code ---"),
                MetaSub.code(),
                Rem("--- Data Objects ---"),
                CodeObject.get_code(),
                L("program_start"),
            ]
            self._built = True
            self.fw = fw
        else:
            fw = self.fw
        return fw

    def show(self):
        pprint.pprint(self.code(), width=1, indent=2)

    def assemble(self):
        fw = Instr.assemble(self.code())
        l = len(fw)
        align = math.ceil(l / 8) * 8
        diff = align - l
        for i in range(diff):
            fw.append(0)
        return fw

    def hex(self):
        asm = self.assemble()
        full_hex = ""
        for i in asm:
            hex_string = "{:04X}".format(i)
            full_hex += hex_string
        return full_hex

    def disassemble(self):
        c = self.assemble()
        a = Assembler()
        return a.disassemble(c)
