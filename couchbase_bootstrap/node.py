import logging

from couchbase_cluster_admin import cluster

from .controller import bootstrap_controller
from .member import bootstrap_member

logger = logging.getLogger(__name__)


def bootstrap_node(cfg):
    node = cluster.Cluster(
        cfg.get("clusterName", None),
        services=cfg["services"],
        api_host=cfg["api_host"],
        api_port=cfg["api_port"],
        username=cfg["username"],
        password=cfg["password"],
    )

    if "disk_paths" in cfg:
        node.set_disk_paths(cfg["disk_paths"])

    node_type = cfg["node_type"]
    if node_type == "controller":
        logger.debug("node type is controller")
        bootstrap_controller(node, cfg)

    elif node_type == "member":
        logger.debug("node type is member")
        bootstrap_member(node, cfg)
