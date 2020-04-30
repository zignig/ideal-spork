# select a board from the following list",

# extracted from https://github.com/nmigen/nmigen-boards
import os, importlib

from jinja2 import Environment, FileSystemLoader

# Board listings
def extract_boards():
    "get a list of all the nmigen_boards"
    import nmigen_boards

    path = nmigen_boards.__path__[0]
    file_list = os.listdir(path)
    board_files = []
    # get a list of the the board files
    for name in file_list:
        if name.endswith(".py"):
            short_name = name.split(".")[0]
            if short_name != "__init__":
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
    return boards.keys()

#Templating

def gen_templates(board_list):
    " with a list of boards generate templates"
    env = Environment(
        loader=FileSystemLoader('templates')
    )
    print(env.loader.list_templates())
    templates = env.loader.list_templates()
    for i in templates:
        print(i)
        tmpl =  env.get_template(i)
        print(board_list)
        render = tmpl.render(board_list)
        print(render)

if __name__ == "__main__":
    boards = extract_boards()
    for board in boards.items():
        info = board_info(board)
    gen_templates(info)
