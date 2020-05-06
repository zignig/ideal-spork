# generate selected files

from jinja2 import Environment, FileSystemLoader
import time, pathlib, os

from ..logger import logger

log = logger(__name__)


class TemplateError(Exception):
    pass


class FileBuilder:
    def __init__(self, board=None, construct=None, devices=None, force=False):
        self.board = board
        self.construct = construct
        self.devices = devices
        self.force = force

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

    def generate(self):
        log.critical("No files generated YET")
        constr = self.construct()
        log.info("Prepare the board info")
        log.critical(self.templates)
        info = {"creation_time": time.ctime()}
        if hasattr(constr, "files"):
            log.critical(constr.files)
            for file_name in constr.files:
                if file_name not in self.templates:
                    raise TemplateError(
                        "Template {:s} does not exist".format(file_name)
                    )
                templ = self.env.get_template(file_name)
                log.debug("Render the file")
                render = templ.render(info)
                target_file = constr.files[file_name]
                log.critical(target_file)
                try:
                    log.debug("Check if the files already exists")
                    stat = os.stat(target_file)
                    log.critical(stat)
                    if self.force:
                        log.critical("OVERWRITE ARRRRGHS")
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


# TODO old, pls remove
def gen_templates(board_list, class_name="MySpork"):
    " with a list of boards generate templates"
    log.info("Generating templated files")
    path = pathlib.Path(__file__).parent.absolute()
    env = Environment(loader=FileSystemLoader(str(path) + os.sep + "templates"))
    templates = env.loader.list_templates()
    cpu = ""
    for t in templates:
        log.critical("rendering template %s", t)
        if t.endswith("tmpl"):
            tmpl = env.get_template(t)
            render = tmpl.render(
                board_list, creation_time=time.ctime(), class_name=class_name, cpu=cpu
            )
            # print(render)
        # print()

    # TODO create files, check for existance and fail on has
