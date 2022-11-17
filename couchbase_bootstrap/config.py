import logging
import os.path
import sys

import yaml

logger = logging.getLogger(__name__)

config_file_paths = [
    "./config.yml",
    "~/.config/couchbase-bootstrap/config.yml",
    "/etc/couchbase-bootstrap/config.yml",
]


class Configuration(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)


#    def __getitem__(self, key):
#        return self.__dict__[key]


def get_config(path=None) -> Configuration:
    # If supplied, treat the first argument as the configuration file.
    if len(sys.argv) > 1:
        config_file_paths.insert(0, sys.argv[1])

    # If supplied, treat the path argument as the configuration file.
    if path is not None:
        config_file_paths.insert(0, path)

    config = None
    for fn in config_file_paths:
        try:
            with open(os.path.expanduser(fn), "r") as f:
                config = yaml.safe_load(f)
                logger.debug("config loaded", extra={"path": fn})
                break
        except FileNotFoundError as e:
            logger.debug("config file not found", extra={"path": fn, "exception": e})

    if config is None:
        logger.error(
            "no config file found",
            extra={
                "attempted_paths": config_file_paths,
            },
        )
        raise RuntimeError(
            f"no config file found; tried: {'; '.join(config_file_paths)}"
        )

    d = Configuration(config)
    logger.debug("got config", extra={"config": d})
    return Configuration(config)
