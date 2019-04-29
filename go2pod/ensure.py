import json
import os
from distutils.version import LooseVersion

import delegator

from go2pod.action import Action
from go2pod.const import PODYAML, CONFIG_YAML, VERSIONFILE
from go2pod.config import Config, ConfigLoadError
from go2pod.docker import DockerClient
from go2pod.kube import KubeClient


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
        action.ensure_true(cmd.ok,
                           "Can't connect to docker daemon",
                           warn_only=True)
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


def ensure_kube():
    with Action('Checking kube apiserver').start() as action:
        cmd = delegator.run('kubectl version')
        action.ensure_true(cmd.ok, "Can't connect to kube apiserver")
    return KubeClient()


def ensure_config():
    with Action('Loading go2pod.yml').start() as action:
        version = None
        with Action('Try to load versionfile').start():
            tmpdir = os.path.join(os.getcwd(), './tmp-go2pod')
            versionfile_path = os.path.join(tmpdir, VERSIONFILE)
            if os.path.exists(versionfile_path):
                with open(versionfile_path) as f:
                    version = f.read().strip()
        try:
            config = Config.load(CONFIG_YAML, version=version)
        except ConfigLoadError as e:
            action.fail(str(e))
    return config


def ensure_tmpdir(create=True):
    """ensure a tmp directory in current workspace

    We will not delete this directory automatically.

    We do not use tempfile to create tempdirectory because
    dockerd may have its own /tmp. For example, when dockerd is
    running under ubuntu snap environment, dockerd will
    have its own tmp directory.
    """
    dirpath = os.path.join(os.getcwd(), './tmp-go2pod')
    with Action('Checking go2pod tmpdir: ./tmp-go2pod').start() as action:
        exists = os.path.exists(dirpath)
        if not exists:
            if create:
                os.mkdir(dirpath)
            else:
                action.fail('go2pod tmpdir not found')
    return dirpath


def ensure_podyaml():
    with Action('Checking ./tmp-go2pod/pod.yaml').start() as action:
        tmpdir = ensure_tmpdir(create=False)
        yaml_path = os.path.join(tmpdir, PODYAML)
        action.ensure_true(os.path.exists(yaml_path))
    return yaml_path
