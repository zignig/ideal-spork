# Regisiter devices into search system

from ..logger import logger

log = logger(__name__)

drivers = {}


class Catalogue:
    " A catalogue of registered things"

    def __init__(self):
        self.sections = {}

    def insert(self, section, name, cls):
        if section not in self.sections:
            self.sections[section] = {name: [cls]}
        else:
            current_section = self.sections[section]
            if name in current_section:
                current_section[name].append(cls)
            else:
                current_section[name] = [cls]


catalog = Catalogue()


def Enroll(**info):
    " Wrapper for registering meta data of constructs "

    def inner(cls):
        for i, j in info.items():
            log.info("Peripheral registration %s %s %s", i, j, cls)
            catalog.insert(i, j, cls)
        return cls

    return inner
