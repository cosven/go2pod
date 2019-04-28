import os

from colorama import init

from go2pod.action import Action
from go2pod.template import gen_dockerfile
from go2pod.ensure import (
    ensure_prerequisites,
    ensure_docker,
    ensure_config,
    ensure_tmpdir,
)
from go2pod.patch import patch_delegator_run


init()
patch_delegator_run()


def build_docker_image(client, config, tmpdir):
    dockerfilepath = os.path.join(tmpdir, 'Dockerfile')
    with open(dockerfilepath, 'w') as f:
        f.write(gen_dockerfile(config))
    with Action('Building docker image').start() as action:
        action.ensure_true(client.build(tmpdir, config.image),
                           'Build docker image failed.')


def main():
    ensure_prerequisites()
    docker_client = ensure_docker()

    config = ensure_config()
    tmpdir = ensure_tmpdir()

    build_docker_image(docker_client, config, tmpdir)
