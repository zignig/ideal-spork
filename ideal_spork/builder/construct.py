# Choose a construct for the board

from ..logger import logger

log = logger(__name__)


def show_available(constructs):
    print("\nConstruct does not exist, choose from the following \n")
    for num, constr in enumerate(constructs):
        print("{:>4}  {}".format(num, constr.__name__))
    print()


def interactive_construct(available, constr):
    log.critical("List choose %s", str(available))
    return constr


def choose_construct(available, constr, board):
    constructs = {}
    for c in available:
        constructs[c.__name__] = c
    if constr not in constructs:
        log.error("Construct does not exist")
        show_available(available)
        raise ValueError("No construct {:s}".format(constr))
    return constructs[constr]
