import logging

from .utils import *

logger = logging.getLogger(__name__)


def bootstrap_controller(node, cfg):
    # Enable services on this node.
    node.enable_services()

    # Set memory quotas per service.
    node.set_memory_quotas(
        cfg["memory_quotas"],
        total_memory_mb=meminfo()["MemTotal"] / 1024**3,
    )

    # Set authentication, and thus transition this node to become the cluster
    # controller.
    node.set_authentication()

    # Update index settings. Setting the storage mode is required before indexes
    # can be created.
    if "index_settings" in cfg:
        node.update_index_settings(cfg["index_settings"])

    # Create buckets.
    for bucket_config in cfg.get("buckets", []):
        logger.info("creating bucket", extra={"config": bucket_config})
        node.create_bucket(bucket_config)

    # Create users.
    for user in cfg.get("users", []):
        logger.info("creating user", extra={"config": user})
        node.create_user(user["username"], user["config"])
