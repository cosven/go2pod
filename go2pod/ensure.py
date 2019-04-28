import json
import os
from distutils.version import LooseVersion

import delegator

from go2pod.action import Action
from go2pod.docker import DockerClient
from go2pod.config import Config, ConfigLoadError


def ensure_prerequisites():
    # check if docker/kubectl exists in path
    with Action('Checking docker executable').start() as action:
        action.ensure_true(delegator.run('which docker').ok,
                           "Can't find docker executable")
    with Action('Checking kubelet executable').start() as action:
        action.ensure_true(delegator.run('which kubectl').ok,
                           "Can't find kubelet executable")


def ensure_docker():
    """
    try to connect to docker daemon and init,
    """
    client = DockerClient()

    cmdstr = "docker version --format '{{json .}}'"
    js = {}
    with Action('Checking docker daemon').start() as action:
        cmd = delegator.run(cmdstr)
        action.ensure_true(cmd.ok, "Can't connect to docker daemon")
        js = json.loads(cmd.out)

    if not cmd.ok:
        with Action('Checking docker daemon with sudo').start() as action:
            cmdstr_sudo = 'sudo ' + cmdstr
            cmd_sudo = delegator.run(cmdstr_sudo)
            action.ensure_true(
                cmd_sudo.ok,
                "Can't connect to docker daemon even with sudo",
            )
            client.need_sudo = True
            js = json.loads(cmd_sudo.out)
            client_version = js['Client']['Version']
            server_version = js['Server']['Version']
    if LooseVersion(client_version) >= LooseVersion('17.05') and\
       LooseVersion(server_version) >= LooseVersion('17.05'):
        client.has_msb_supported = True
    return client


def ensure_config():
    with Action('Loading go2pod.yml').start() as action:
        try:
            config = Config.load('go2pod.yml')
        except ConfigLoadError as e:
            action.fail(str(e))
    return config


def ensure_tmpdir():
    """create a tmp directory in current workspace

    We will not delete this directory automatically.

    We do not use tempfile to create tempdirectory because
    dockerd may have its own /tmp. For example, when dockerd is
    running under ubuntu snap environment.
    """
    dirpath = os.path.join(os.getcwd(), './tmp-go2pod')
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath
