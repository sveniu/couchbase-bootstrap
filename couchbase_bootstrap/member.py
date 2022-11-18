import logging

import backoff
import requests
from couchbase_cluster_admin import cluster

logger = logging.getLogger(__name__)

join_timeout_seconds = 3600


def lookup_join_timeout_seconds():
    return join_timeout_seconds


@backoff.on_exception(
    backoff.expo,
    (
        cluster.AddToNotProvisionedNodeException,
        requests.exceptions.ConnectionError,
    ),
    max_time=lookup_join_timeout_seconds,
)
def join_cluster(node, config):
    logger.info("attempting to join cluster")
    node.join_cluster(
        config["cluster_controller_address"],
        config["cluster_controller_port"],
        insecure=config["insecure_join"],
    )


def bootstrap_member(node, cfg):
    # Set join timeout for use by the backoff decorator.
    if "join_timeout_seconds" in cfg:
        global join_timeout_seconds
        join_timeout_seconds = cfg["join_timeout_seconds"]

    # Join the cluster, with backoff.
    join_cluster(node, cfg)

    logger.info("cluster join successful")
