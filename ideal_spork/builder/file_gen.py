# generate selected files

from jinja2 import Environment, FileSystemLoader
import time, pathlib

from ..logger import logger

log = logger(__name__)


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
