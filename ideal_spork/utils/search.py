# Regisiter devices into search system

from ..logger import logger

log = logger(__name__)

drivers = {}


class Catalogue:
    def __init__(self):
        self.sections = []


def Register(**info):
    def inner(cls):
        for i, j in info.items():
            log.info("Peripheral registration %s %s", i, j)
            if i in drivers:
                drivers[i].append((j, cls))
            else:
                drivers[i] = [(j, cls)]
        return cls

    return inner
