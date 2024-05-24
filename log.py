import logging

class Logger:
    def __init__(self, log_file: str = __name__, filemode: str = 'a', debug_level = logging.DEBUG) -> None:
        logger = logging.getLogger(__name__)
        logger.setLevel(debug_level)
        handler = logging.FileHandler(f'{log_file}.log', filemode)
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)

    def critical(self, msg: str) -> None:
        self.logger.critical(msg)
