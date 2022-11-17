import logging

logger = logging.getLogger(__name__)


def bootstrap_controller(node, cfg):
    # Enable services on this node.
    node.enable_services()

    # Set memory quotas per service.
    node.set_memory_quotas(cfg["memory_quotas"])

    # Set authentication, and thus transition this node to become the cluster
    # controller.
    node.set_authentication()

    # Create buckets.
    for bucket_config in cfg.get("buckets", []):
        logger.info("creating bucket", extra={"config": bucket_config})
        node.create_bucket(bucket_config)

    # Create users.
    for user in cfg.get("users", []):
        logger.info("creating user", extra={"config": user})
        node.create_user(user["username"], user["config"])
