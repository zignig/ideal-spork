import logging, sys

log_level = logging.ERROR

fomattingter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(name)s -  %(funcName)s - %(lineno)s - %(message)s"
)
# fomattingter = logging.Formatter( fmt="%(asctime)s - %(levelname)s %(name)s.%(funcName)s - %(message)s")

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(fomattingter)
root_logger = logging.getLogger()
root_logger.addHandler(handler)
root_logger.setLevel(log_level)


def logger(name):
    return root_logger.getChild(name)


def set_logging_level(set_level):
    root_logger.setLevel(set_level)
