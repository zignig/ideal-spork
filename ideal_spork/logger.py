import logging

log_level = logging.INFO


def logger(name):
    # fomattingter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    fomattingter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s %(name)s.%(funcName)s - %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(fomattingter)

    logger = logging.getLogger(name)

    logger.addHandler(handler)
    logger.setLevel(log_level)

    return logger


def level(set_level):
    log_level = set_level
