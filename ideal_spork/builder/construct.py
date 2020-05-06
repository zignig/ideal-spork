# Choose a construct for the board

from ..logger import logger
from .interactive import select_from_list

log = logger(__name__)


def show_available(constructs):
    print("\nConstruct does not exist, choose from the following \n")
    for num, constr in enumerate(constructs):
        print("{:>4}  {}".format(num, constr.__name__))
    print()


def interactive_construct(available, constr):
    log.info("List choose %s", str(available))
    construct_info = []
    for i in available:
        detail = "{:s} - {:s}".format(i.__name__, i.__doc__)
        construct_info.append(detail)
    val = select_from_list(construct_info, name="Construct", as_num=True)
    return available[val]


def check_construct(available, constr):
    constructs = {}
    for c in available:
        constructs[c.__name__] = c
    if constr not in constructs:
        log.error("Construct does not exist")
        show_available(available)
        return None
    return constructs[constr]
