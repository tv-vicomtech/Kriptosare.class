import sys
import docker
import time
from getopt import getopt
from random import randint
from decimal import Decimal

def collector_setup():


    client = docker.from_env()
    print(" ********datafeed*****")
    client.images.build(path="data", tag="datafeed")

    return client

def generate_collector(client):
    """
    Runs a new container.
    :param client: docker client
    :param network_name: docker network name
    :param node_num: node id
    :return:
    """
    containers = client.containers

    CMD = "/etc/init.d/script.sh"
    port = {'9042':9042}

    print("DATAFEED")
    containers.run(
        "datafeed",
        CMD,
        name="datafeed",
        detach=True,
        ports=port)

if __name__ == '__main__':

    client = collector_setup()
    generate_collector(client)
    print("*****OK*****")

