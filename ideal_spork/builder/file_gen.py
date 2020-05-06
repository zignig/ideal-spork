# generate selected files

from jinja2 import Environment, FileSystemLoader
import time, pathlib, os

from ..logger import logger

log = logger(__name__)


class TemplateError(Exception):
    pass


class FileBuilder:
    def __init__(
        self, name=None, board=None, construct=None, devices=None, force=False
    ):
        self.board = board
        self.construct = construct
        self.devices = devices
        self.force = force
        self.name = name

        log.info("Loading template files")

        path = pathlib.Path(__file__).parent.absolute()
        self.env = Environment(
            loader=FileSystemLoader(str(path) + os.sep + "templates")
        )
        self.templates = self.env.loader.list_templates()

    def write_file(self, target_file, render):
        f = open(target_file, "w")
        f.write(render)
        f.close()

    def build(self):
        self.collate()
        self.generate()

    def collate(self):
        log.critical("Collate information for templating")
        import yaml

        print(self.devices.devices)

    def generate(self):
        constr = self.construct()
        log.info("Prepare the board info")
        log.info(self.board)
        info = {
            "creation_time": time.ctime(),
            "module": self.board["module"],
            "board_name": self.board["class_name"],
            "class_name": self.name,
        }
        if hasattr(constr, "files"):
            log.debug(constr.files)
            for file_name in constr.files:
                if file_name not in self.templates:
                    raise TemplateError(
                        "Template {:s} does not exist".format(file_name)
                    )
                templ = self.env.get_template(file_name)
                log.debug("Render the file %s", file_name)
                render = templ.render(info)
                target_file = constr.files[file_name]
                # empty file name is changed to the name target
                if target_file == None:
                    target_file = self.name.lower() + ".py"
                log.info(target_file)
                try:
                    log.debug("Check if the files already exists")
                    stat = os.stat(target_file)
                    log.debug(stat)
                    if self.force:
                        log.critical("Over writing file {:s}".format(target_file))
                        self.write_file(target_file, render)
                    else:
                        log.critical(
                            "File {:s} already exists, will not overwrite".format(
                                target_file
                            )
                        )
                        raise TemplateError("File {:s} exists".format(file_name))
                except:
                    self.write_file(target_file, render)
