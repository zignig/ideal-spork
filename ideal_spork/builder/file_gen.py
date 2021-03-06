# generate selected files

from jinja2 import Environment, FileSystemLoader
import time, pathlib, os

from ..logger import logger

log = logger(__name__)

# print extra information ( not logged )
debug = False


class TemplateError(Exception):
    pass


class TemplateInfo:
    " Class to hold all the templating information "

    def __init__(self):
        object.__setattr__(self, "sections", [])

    def __setattr__(self, name, value):
        log.debug("{:s} {:s}".format(str(name), str(value)))
        if hasattr(self, name):
            raise TemplateError("Template section already exists")
        object.__setattr__(self, name, value)
        self.sections.append(name)

    def as_dict(self):
        the_dict = {}
        for i in self.sections:
            val = getattr(self, i)
            log.debug("Template -> {:s} - {:s}".format(i, str(val)))
            the_dict[i] = val
        return the_dict


class FileBuilder:
    def __init__(
        self,
        name=None,
        board=None,
        construct=None,
        devices=None,
        force=False,
        local=False,
    ):
        self.board = board
        self.construct = construct
        self.devices = devices
        self.force = force
        self.name = name
        self.local = local

        # internal Constructions
        self.info = TemplateInfo()

        log.info("Loading template files")

        path = pathlib.Path(__file__).parent.absolute()
        self.env = Environment(
            loader=FileSystemLoader(str(path) + os.sep + "templates")
        )
        self.templates = self.env.loader.list_templates()
        for templ in self.templates:
            log.debug("template file {:s}".format(templ))

    def write_file(self, target_file, render):
        # TODO error handling
        log.warning("Writing target file {:s}".format(target_file))
        f = open(target_file, "w")
        f.write(render)
        f.close()

    def build(self):
        self.collate()
        self.generate()

    def collate(self):
        log.info("Collate information for templating")

        # Create imports for the peripherals
        dev = self.devices.peripherals
        import_list = []
        dev_list = []

        def import_name(inst):
            if self.local:
                # TODO need to generate local import paths and copy files into place
                log.critical("Local UNFINISHED")
                raise TemplateError("No local yet")
            else:
                data = "from {:s} import {:s}".format(
                    str(inst.__module__), str(inst.__name__)
                )
            return data

        # collect driver list and compare to remove duplicates
        driver_list = []
        driver_class = None
        for i in dev:
            log.debug("Device {:s}".format(str(i)))
            if len(i[1]) > 1:
                log.critical(
                    "{:s} has multiple drivers, using {:s}".format(
                        i[0], str(i[1][-1].__name__)
                    )
                )
                driver_class = i[1][-1]
            else:
                driver_class = i[1][0]

            if driver_class in driver_list:
                log.warning(
                    "Driver {:s} already installed not adding".format(str(driver_class))
                )
            else:
                driver_list.append(driver_class)
                import_list.append(import_name(driver_class))

        self.info.imports = import_list

    def generate(self):
        constr = self.construct()
        log.info("Prepare the board info")
        log.info(self.board)
        # Add the extra information into info block
        self.info.creation_time = time.ctime()
        self.info.module = self.board["module"]
        self.info.board_name = self.board["class_name"]
        self.info.class_name = self.name

        if hasattr(constr, "files"):
            log.debug("Template files {:s}".format(str(constr.files)))
            for file_name in constr.files:
                if file_name not in self.templates:
                    raise TemplateError(
                        "Template {:s} does not exist".format(file_name)
                    )
                templ = self.env.get_template(file_name)
                log.debug("Render the file {:s}".format(file_name))
                # Render the file
                render = templ.render(self.info.as_dict())
                if debug:
                    print(render)
                target_file = constr.files[file_name]
                # empty file name is changed to the name target
                if target_file == None:
                    target_file = self.name.lower() + ".py"
                log.info("Template::{:s}".format(target_file))
                try:
                    log.debug("Check if the files already exists")
                    stat = os.stat(target_file)
                    log.debug(stat)
                    if self.force:
                        log.warning("Over writing file {:s}".format(target_file))
                        self.write_file(target_file, render)
                    else:
                        log.critical(
                            "File {:s} already exists, will not overwrite, use -f to force".format(
                                target_file
                            )
                        )
                except:
                    self.write_file(target_file, render)
