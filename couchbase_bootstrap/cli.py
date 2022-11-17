import logging
import sys
import traceback

from .config import get_config
from .log import CustomJsonFormatter
from .node import bootstrap_node

logger = logging.getLogger()


def main():
    cfg = get_config()

    # Update log level from config.
    logger.setLevel(cfg.get("log_level", logging.INFO))

    return bootstrap_node(cfg)


def cli():
    logHandler = logging.StreamHandler(sys.stdout)
    formatter = CustomJsonFormatter("%(timestamp)s %(name)s %(level)s %(message)s")
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.NOTSET)

    try:
        main()
    except Exception as e:
        logger.error(
            "unhandled exception; exiting",
            extra={"exception": e, "traceback": traceback.format_exc()},
        )
        sys.exit(1)
