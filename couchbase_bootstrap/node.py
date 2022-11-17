import logging

from couchbase_cluster_admin import cluster

from .controller import bootstrap_controller
from .member import bootstrap_member

logger = logging.getLogger(__name__)


def bootstrap_node(cfg):
    node = cluster.Cluster(
        cfg.get("clusterName", None),
        services=cfg["services"],
        host=cfg["api_host"],
        port=cfg["api_port"],
        username=cfg["username"],
        password=cfg["password"],
    )

    if "disk_paths" in cfg:
        node.set_disk_paths(cfg["disk_paths"])

    node_type = cfg["node_type"]
    if node_type == "controller":
        bootstrap_controller(node, cfg)

    elif node_type == "member":
        bootstrap_member(node, cfg)
