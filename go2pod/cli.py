import os

from colorama import init

from go2pod.action import Action
from go2pod.template import gen_dockerfile, gen_pod_yaml
from go2pod.ensure import (
    ensure_prerequisites,
    ensure_docker,
    ensure_config,
    ensure_tmpdir,
)
from go2pod.kube import KubeClient
from go2pod.patch import patch_delegator


init()
patch_delegator()


def build_docker_image(client, config, tmpdir):
    dockerfile_path = os.path.join(tmpdir, 'Dockerfile')
    with open(dockerfile_path, 'w') as f:
        f.write(gen_dockerfile(config))
    action_desc = 'Building docker image, this may take several minutes'
    with Action(action_desc).start() as action:
        action.ensure_true(client.build(tmpdir, config.image),
                           'Build docker image failed.')


def push_docker_image(client, config):
    client.push(config.image)


def create_pod(client, config, tmpdir):
    podyaml_path = os.path.join(tmpdir, 'pod.yaml')
    with open(podyaml_path, 'w') as f:
        f.write(gen_pod_yaml(config))
    with Action('Sending pod creation request').start() as action:
        action.ensure_true(client.apply_yaml(podyaml_path))


def main():
    ensure_prerequisites()
    docker_client = ensure_docker()
    kube_client = KubeClient()

    config = ensure_config()
    tmpdir = ensure_tmpdir()

    build_docker_image(docker_client, config, tmpdir)
    push_docker_image(docker_client, config)
    create_pod(kube_client, config, tmpdir)
