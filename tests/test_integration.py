import json
import subprocess
import time

import jmespath
import pytest
import requests

from couchbase_bootstrap import config
from couchbase_bootstrap import node as mnode

# https://docs.couchbase.com/server/current/install/install-ports.html#detailed-port-description
COUCHBASE_PORT_REST = 8091


@pytest.fixture(scope="session")
def docker_compose_file_path(pytestconfig):
    paths = (
        pytestconfig.rootpath / "tests" / "docker-compose.yml",
        pytestconfig.rootpath / "docker-compose.yml",
    )

    for path in paths:
        if path.is_file():
            return path

    raise FileNotFoundError(f"Could not find docker-compose.yml; tried {paths}")


@pytest.fixture(scope="session")
def docker_inspect(docker_compose_file_path):
    subprocess.check_call(
        [
            "docker-compose",
            "-f",
            docker_compose_file_path,
            "up",
            "-d",
        ]
    )

    yield json.loads(
        subprocess.check_output(
            ["docker", "inspect", "couchbase_node_a", "couchbase_node_b"]
        )
    )

    subprocess.check_call(
        [
            "docker-compose",
            "-f",
            docker_compose_file_path,
            "down",
        ]
    )


def test_integration(docker_inspect):
    node_a = {
        "host": "127.0.0.1",
        "port": jmespath.search(
            '[0].HostConfig.PortBindings."8091/tcp"[0].HostPort', docker_inspect
        ),
        "internal_ip": jmespath.search(
            "[0].NetworkSettings.Networks.*.IPAddress", docker_inspect
        )[0],
    }
    node_b = {
        "host": "127.0.0.1",
        "port": jmespath.search(
            '[1].HostConfig.PortBindings."8091/tcp"[0].HostPort', docker_inspect
        ),
        "internal_ip": jmespath.search(
            "[1].NetworkSettings.Networks.*.IPAddress", docker_inspect
        )[0],
    }

    # Wait for nodes to start.
    for node in (node_a, node_b):
        while True:
            url = f"""http://{node["host"]}:{node["port"]}/ui/index.html"""
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    break
            except requests.exceptions.ConnectionError:
                pass

            time.sleep(0.5)

    config_a = config.get_config("tests/config_a.yml")
    config_b = config.get_config("tests/config_b.yml")

    # Use internal Docker IP for the controller node.
    config_b["cluster_controller_address"] = node_a["internal_ip"]
    config_b["cluster_controller_port"] = f"{COUCHBASE_PORT_REST}"

    mnode.bootstrap_node(config_a)
    mnode.bootstrap_node(config_b)
