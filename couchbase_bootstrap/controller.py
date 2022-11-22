import logging
from pathlib import Path

from .utils import *

logger = logging.getLogger(__name__)


def bootstrap_controller(node, cfg):
    # Enable services on this node.
    node.enable_services()

    # Set memory quotas per service.
    node.set_memory_quotas(
        cfg["memory_quotas"],
        total_memory_mb=meminfo()["MemTotal"] / 1024**2,
    )

    # Set authentication, and thus transition this node to become the cluster
    # controller.
    node.set_authentication()

    # Update index settings. Setting the storage mode is required before indexes
    # can be created.
    if "index_settings" in cfg:
        logger.debug("updating index settings")
        node.update_index_settings(cfg["index_settings"])

    # Create buckets.
    for bucket_config in cfg.get("buckets", []):
        logger.info("creating bucket", extra={"config": bucket_config})
        node.create_bucket(bucket_config)

    # Create users.
    for user in cfg.get("users", []):
        logger.info("creating user", extra={"config": user})
        node.create_user(user["username"], user["config"])

    # Run cbq scripts.
    for entry in cfg.get("cbq_scripts", []):
        dir = Path(entry["directory"])
        for fn in dir.iterdir():
            if not fn.is_file():
                continue

            # Execute the script.
            logger.debug("executing cbq script", extra={"entry": entry})
            exec_cbq_script(
                entry["engine"],
                entry["username"],
                entry["password"],
                fn,
            )
