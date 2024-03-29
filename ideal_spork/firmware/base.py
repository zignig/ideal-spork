# attempt at a register allocator
from collections import OrderedDict
import random
import pprint
import weakref

from ..cores.periph.bus import RegMap

from ..logger import logger

log = logger(__name__)

__all__ = [
    "LocalLabels",
    "SubR",
    "Window",
    "MetaSub",
    "Rem",
    "Block",
    "CodeObject",
    "Inline",
    "FWError",
]

"""
ideas

allocate variables into a register bank, break it into windows 
limit the total number of windows and spill into ram if needed

work out how to make sure that the variables are in the correct window
for actions 

minimise the amount of spill an copying from one window to the other

? contiguous windows
? linked list of windows
? dynamic window allocation

multi register allocations ? 
pointer deferencing ? 

###

from conversations with tpwrules and looking at his programming style.
The use of a frame stack where each subroutine call moves the register window 
up 8 registers.

- Loads the needed registers from the preceeding frame
- Allocates local variables 
- Runs the subroutine code
- And then return jumps from the parent frame.
- The parent routine can then pluck register values out of the child frame.

This is quite elegant. A subroutine becomes.

assuming R6 is the Frame pointer (fp)

If you need to pass variables up and down

    LD(var1,fp,1) # load the first register of the previous frame into var1 
    LD(var2,fp,2) # second register
    ADJW(-8) # move the window up 
    LDW(fp,-8) # put the previous window address into R6

    # other code
    # blah blah blah


    Then return up
    ADJW(8) # move the window to the previous frame address
    JR(R7,0) # the return jump is in the parent frame

    ST(return_val,fp,-3) # put the value it register 3 in the frame above

If nothing needs to be passed up or down

    ADJW(8)
    # blah blah blah 
    ADJW(-8)
    JR(R7,0)

and you don't lose a register for the frame pointer.

When you want to call a subroutine , it's just

    JAL(R7,'subroutine')

and tada, it runs and makes the registers available to the above frame.

Kind of nifty.

rehack of https://github.com/tpwrules/ice_panel/blob/master/bonetools.py

"""

from boneless.arch.opcode import *
from boneless.arch.instr import Instr


class RegError(Exception):
    pass


class NameCollision(RegError):
    pass


class WindowFull(RegError):
    pass


class BadParamCount(RegError):
    pass


class FWError(Exception):
    pass


class PostFix:
    _postfixes = []

    def __init__(self):
        self.postfix = None

    def __call__(self, postfix=None, bits=16):
        counter = 0
        while True:
            if not postfix:
                postfix = "_{:04X}".format(random.randrange(2 ** bits))
            if postfix not in PostFix._postfixes:
                PostFix._postfixes += postfix
                return postfix
            counter += 1
            if counter > 100:
                raise FWError("Too many prefixes %s", postfix)


# a postfix generator
Postfix = PostFix()


class CodeObject:
    " For adding data objects to the firmware "
    _objects = []

    def __init__(self):
        CodeObject._objects.append(self)
        object.__setattr__(self, "_postfix", Postfix())

    @classmethod
    def get_code(cls):
        l = []
        for i in cls._objects:
            if i._used == True:
                l.append(i.code())
        return l


class Inline:
    " Define an inline function "

    def __init__(self, window, ll=None):
        self.w = window
        if ll is not None:
            self.ll = ll
        else:
            self.ll = LocalLabels()

    def instr(self):
        raise FWError("Inline class needs 'instr' defined return a [] of asm")

    def __call__(self):
        return self.instr()


class Rem:
    " for adding remarks in code "

    def __init__(self, val):
        self.val = val

    def __call__(self, m):
        return []

    def __repr__(self):
        return 'Rem("' + str(self.val) + '")'


class Block:
    " A Block of code "
    pass


class LocalLabels:
    """ Local random labels for inside subr
        create a local labeler
        ll = LocalLabels()
        make a label - ll('test')
        reference the label - ll.test
    """

    def __init__(self):
        self._postfix = Postfix()
        self._names = {}

    def __call__(self, name):
        self._names[name] = name + self._postfix
        setattr(self, name, name + self._postfix)
        return L(name + self._postfix)

    def __getattr__(self, key):
        if key in self._names:
            return self._names[key]
        # for forward declarations
        self._names[key] = key + self._postfix
        setattr(self, key, key + self._postfix)
        return self._names[key]


class Window:
    " Allocatable register window "

    _REGS = [R0, R1, R2, R3, R4, R5, R6, R7]
    _size = 8

    def __init__(self, jumper=True):
        self._allocated = [False] * 8
        self._name = [""] * 8
        if jumper:
            # frame for subroutine calls R6 is fp , R7 is return
            self._allocated[6] = True
            self._name[6] = "fp"
            setattr(self, "fp", self._REGS[6])

            self._allocated[7] = True
            self._name[7] = "ret"
            setattr(self, "ret", self._REGS[7])

    def req(self, name):
        if type(name) == type(""):
            self._single(name)
        if type(name) == type([]):
            for i in name:
                self._single(i)

    def _single(self, name):
        for i in range(self._size):
            if self._allocated[i] == False:
                # free register
                self._allocated[i] = True
                self._name[i] = name
                if name not in self.__dict__:
                    setattr(self, name, self._REGS[i])
                    return
                else:
                    raise NameCollision(self)
        # no free registers
        # fail for now
        raise WindowFull(self)

    def __getitem__(self, key):
        if hasattr(self, key):
            return self.__dict__[key]

    # TODO spill and reuse registers


class VectorTable:

    " Vector Table "

    _size = 8

    def __init__(self, name="no_name"):
        self.labels = OrderedDict()
        self.name = name

    def __getattr__(self, key):
        if key in self.labels:
            print("get ", key)
            return self.lables[key]

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key not in ["labels", "name"]:
            print("set ", key, " to ", value)
            self.labels[key] = value

    def dump(self):
        data = []
        for i in self.labels.items():
            data.append([L(i[0]), AR(i[1])])
        l = len(data)
        if l < self._size:
            for i in range(self._size - l):
                data.append([0])
        return data


class MetaSub(type):
    subroutines = []
    """
    Meta Sub is a class for collecting all the routines together
    It also expands the useds subroutines for adding in the epilogue of the
    program
    """

    def __new__(cls, clsname, bases, attrs):
        newclass = super(MetaSub, cls).__new__(cls, clsname, bases, attrs)
        cls.register(newclass)  # here is your register function
        return newclass

    def register(cls):
        d = MetaSub.subroutines
        if cls.__qualname__ == "SubR":
            # Don't add root subclass
            return
        if cls not in d:
            d.append(cls())

    @classmethod
    def code(cls):
        li = MetaSub.subroutines
        # loop through and add sub-subroutines to the list
        c = []
        while True:
            old_c = c
            c = []
            for i in li:
                if i._called:
                    c.append(i.code())
            if len(old_c) == len(c):
                break
        return c


class SubR(metaclass=MetaSub):
    """
    Calling Standard
    R7 = return address (used by the child frame)
    R6 = frame pointer

    Call structure 
    
    1. copy registers up into frame
    2. jump into subroutine
    3. shift window up
    4. run code
    5. shift window down
    6. return from jump
    7. copy data from upper frame 

    """

    debug = True

    _called = False

    def __init__(self, **kwargs):
        self.w = Window()
        # return registers to upper window
        self._ret = False
        self._ret_target = []
        self.setup()
        self._size = 8  # for later ( stack frames ) TODO
        if not hasattr(self, "name"):
            self.name = type(self).__qualname__
        if hasattr(self, "params"):
            self.length = len(self.params)
            for i in self.params:
                self.w.req(i)
        else:
            self.length = 0
        if hasattr(self, "locals"):
            for i in self.locals:
                self.w.req(i)
        if hasattr(self, "ret"):
            self._ret_len = len(self.ret)
            self._ret = True
            for i in self.ret:
                # return registers can be existing registers
                if i not in self.w.__dict__:
                    self.w.req(i)

        self.build()

    @classmethod
    def mark(cls):
        " include code if the subroutine has been called "
        #        print("marked",cls)
        cls._called = True

    def setup(self):
        raise FWError("Need to set up subroutine , params , locals and ret")

    def build(self):
        # build the objects and stuff
        pass

    def __call__(self, *args, **kwargs):
        if len(args) != self.length:
            raise ValueError("Parameter count is should be '{}'".format(self.length))
        # load the parameters into the next frame
        instr = []
        for i, j in enumerate(args):
            source = j
            target = self.w[self.params[i]].value
            if self.debug:
                instr += [Rem("Load " + self.params[i])]
            instr += [ST(source, self.w.fp, -self._size + target)]

        instr += [JAL(self.w.ret, self.name)]

        # TODO fix register passing
        # This adds a code to copy registers down a window
        # if requested with a ret=[return,register] in the call
        if "ret" in kwargs:
            if self._ret:
                self._ret_target = []
                vals = kwargs["ret"]
                if type(vals) == type([]):
                    if len(vals) > self._ret_len:
                        raise ValueError("To many returns")
                    for i, j in enumerate(vals):
                        source = self.w[self.ret[i]]
                        instr += [Rem("Return " + self.ret[i])]
                        instr += [LD(j, self.w.fp, -self._size + source.value)]
                else:
                    source = vals
                    target = self.w[self.ret[0]].value
                    instr += [Rem("Return " + self.ret[0])]
                    instr += [LD(source, self.w.fp, -self._size + target)]

            else:
                raise ValueError("No return registers exist")

        if False:  # self.debug:
            " clean up the above frame "
            instr += [MOVI(self.w.ret, 0)]
            for i in range(8, 0, -1):
                instr += [ST(self.w.ret, self.w.fp, -i)]
        self.mark()
        return instr

    def instr(self):
        " empty code "
        return []

    def code(self):
        data = [L(self.name)]
        if self.__doc__ is not None:
            data.append(Rem(self.__doc__))
        if self.debug:
            data += [Rem(self.w._name)]
        data += [ADJW(-self._size)]  # window shift up
        data += [LDW(self.w.fp, 0)]  # save window
        # TODO process this line by line, insert spills above
        data += self.instr()
        data += [ADJW(self._size), JR(R7, 0)]  # shift window down
        return [data]


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
        # attach the io_map to all the subroutines
        SubR.reg = self.reg
        Inline.reg = self.reg
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
