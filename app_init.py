import os
import logging.config


def init_logger(app):
    conf = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(levelname)8s - %(message)s",
                 "datefmt": "%d-%m-%Y %H:%M:%S"},
            "extended": {
                "format": "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "file_handler_WEBHOOK": {
                "level": "INFO",
                "class": "logging.handlers.WatchedFileHandler",
                "formatter": "simple",
                "filename": os.path.join(app.config["LOG_DIR"], "webhook.log"),
                "mode": "a",
                "encoding": "utf-8",
            },
            "file_handler_ROOT": {
                "level": "WARNING",
                "class": "logging.handlers.WatchedFileHandler",
                "formatter": "extended",
                "filename": os.path.join(app.config["LOG_DIR"], "root.log"),
                "mode": "a",
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "WEBHOOK": {"level": "NOTSET", "handlers": ["file_handler_WEBHOOK", "console"], "propagate": False},
        },
        "root": {"level": "NOTSET", "handlers": ["console"]},
    }
    if not os.path.exists(app.config["LOG_DIR"]):
        os.mkdir(app.config["LOG_DIR"])
    logging.config.dictConfig(conf)