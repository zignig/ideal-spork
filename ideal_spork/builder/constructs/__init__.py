class Construct:
    pass


from .empty import Empty
from .board_only import BoardOnly
from .boneless import Boneless
from .csr import CSR
from .sequencer import Sequencer
from .blinky import Blinky

available = [Empty, BoardOnly, Boneless, CSR, Sequencer, Blinky]
