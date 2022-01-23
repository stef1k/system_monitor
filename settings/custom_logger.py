import logging
import sys
from pathlib import Path
from loguru import logger
from . import logger_config


class InterceptHandler(logging.Handler):
    loglevel_mapping = {50: 'CRITICAL', 40: 'ERROR', 30: 'WARNING', 20: 'INFO', 10: 'DEBUG', 0: 'NOTSET'}

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class Logger:

    @classmethod
    def make_logger(cls, config_name: str = 'logger'):
        try:
            config = logger_config
            logging_config = config.get(config_name)

            _logger = cls.customize_logging(
                logging_config.get('path'), level=logging_config.get('level'),
                retention=logging_config.get('retention'), _format=logging_config.get('format'),
                rotation=logging_config.get('rotation'),
                default_loggers_to_change=logging_config.get('default_loggers_to_change', []))

            return _logger
        except Exception as e:
            logger.exception(e)
            logger.warning('return default logger')
            return logger

    @staticmethod
    def customize_logging(filepath: Path, level: str, rotation: str, retention: str, _format: str,
                          default_loggers_to_change: list):
        logger.remove()
        logger.add(sys.stdout, enqueue=True, backtrace=True, level=level.upper(), format=_format)

        logger.add(str(filepath), rotation=rotation, retention=retention, enqueue=True, backtrace=True,
                   level=level.upper(), format=_format)

        # logging.basicConfig(handlers=[InterceptHandler()], level=0)
        # logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in default_loggers_to_change:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)
