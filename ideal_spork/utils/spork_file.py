# handler for the spork file

import yaml

from ..logger import logger

log = logger(__name__)


def load_spork(file_name):
    data = yaml.load(open(file_name).read())
    log.critical(data)
    the_spork = ASpork(data)
    return the_spork


class ASpork:
    def __init__(self, attr):
        self.data = attr.keys()
        log.info("Spork file entries %s", attr)
        for i in attr:
            log.debug(i)
            setattr(self, i, attr[i])