import logging


class Logger:
    def __init__(self, log_file: str, filemode: str, debug_level: logging._Level) -> None:
        logging.basicConfig(filename=log_file, filemode=filemode, level=debug_level,
                            format="[%(asctime)s] %(levelname)s %(message)s")

    @staticmethod
    def send_debug(msg: str) -> None:
        logging.debug(msg)

    @staticmethod
    def send_info(msg: str) -> None:
        logging.info(msg)

    @staticmethod
    def send_warn(msg: str) -> None:
        logging.warning(msg)

    @staticmethod
    def send_error(msg: str) -> None:
        logging.error(msg)

    @staticmethod
    def send_critical(msg: str) -> None:
        logging.critical(msg)
