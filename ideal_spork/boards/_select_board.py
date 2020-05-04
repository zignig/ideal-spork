# select a board from the following list",

# extracted from https://github.com/nmigen/nmigen-boards
import os, importlib

from jinja2 import Environment, FileSystemLoader
import time, pathlib

from ..logger import logger

log = logger(__name__)

_boards_built = False

# Board listings


def extract_boards():
    "get a list of all the nmigen_boards"

    global _boards_built

    import nmigen_boards

    path = nmigen_boards.__path__[0]
    file_list = os.listdir(path)
    board_files = []
    # get a list of the the board files
    # display debug once
    for name in file_list:
        if name.endswith(".py"):
            short_name = name.split(".")[0]
            if short_name != "__init__":
                if not _boards_built:
                    log.debug("Found board %s", name)
                    _boards_built = True
                board_files.append(short_name)

    name_dict = {}
    # get the platform names
    for i in board_files:
        board = importlib.import_module(nmigen_boards.__package__ + "." + i)
        platforms = board.__all__
        for j in platforms:
            b = board.__dict__[j]
            name_dict[j] = b
    return name_dict


def get_board(name):
    " get board by name"
    boards = extract_boards()
    if name in boards:
        return (name, boards[name])


def board_info(board):
    "get board information for templating"
    # Board name
    name = board[0]
    # Create an instance
    module = board[1].__module__
    return {"name": name, "module": module}


def short_list():
    " return a list of the board names"
    boards = extract_boards()
    return list(boards.keys())


# Interactive

prolog = """
----------------------------------------------------------------------------------
                                       SPORK!

By Answering the following questions...

 ideal_spork will generate files to make files for nmigen_* 

----------------------------------------------------------------------------------
"""


def select_board():
    " select one board from all available boards"
    boards = short_list()
    count = len(boards)
    val = 0
    while True:
        print("Please select a board")
        print()
        for num, board in enumerate(boards):
            print("{:>4}  {}".format(num, board))
        print()
        val = input("Select from " + str(count) + " boards >")
        try:
            val = int(val)
        except:
            print("Not a number")
            continue
        if val > count:
            print("Selection out of range")
            continue
        break
    return boards[val]


def get_name(prompt, default):
    " ask for a name with defaults"
    val = input(prompt + " (default=" + default + ") >")
    if val == "":
        val = default
    return val


def interactive():
    " interactive board builder"
    print(prolog)
    print()
    board = select_board()
    board_list = extract_boards()
    if board in board_list:
        current_board = (board, board_list[board])
        current_board_info = board_info(current_board)
    else:
        print("Board does not exist")
        log.critical("Board not found %s", board)
        return
    name = get_name("Construct class name", "MySpork")
    gen_templates(current_board_info, name)


def check_board(name):
    boards = extract_boards()
    if name in boards:
        info = board_info(get_board(name))
        gen_templates(info)
    else:
        print("Board does not exist, Select from:")
        boards = short_list()
        for board in boards:
            print(board)


# Templating


def gen_templates(board_list, class_name="MySpork"):
    " with a list of boards generate templates"
    log.info("Generating templated files")
    path = pathlib.Path(__file__).parent.absolute()
    env = Environment(loader=FileSystemLoader(str(path) + os.sep + "templates"))
    templates = env.loader.list_templates()
    cpu = ""
    for t in templates:
        log.debug("rendering template %s", t)
        if t.endswith("tmpl"):
            tmpl = env.get_template(t)
            render = tmpl.render(
                board_list, creation_time=time.ctime(), class_name=class_name, cpu=cpu
            )
            print(render)
        print()
    # TODO create files, check for existance and fail on has


# if main
if __name__ == "__main__":
    boards = extract_boards()
    for board in boards.items():
        info = board_info(board)
    interactive()
