from go2pod.action import Action
from go2pod.ensure import (
    ensure_config,
    ensure_docker,
    ensure_tmpdir,
)


def build_docker_image(client, config, tmpdir):
    action_desc = 'Build docker image, this may take several minutes'
    with Action(action_desc).start() as action:
        action.ensure_true(client.build(tmpdir, config.image),
                           'Build docker image failed.')


def push_docker_image(client, config):
    with Action('Pushing docker image').start() as action:
        action.ensure_true(client.push(config.image),
                           'Push docker image failed.')


def run():
    docker_client = ensure_docker()
    config = ensure_config()
    tmpdir = ensure_tmpdir()
    build_docker_image(docker_client, config, tmpdir)
    push_docker_image(docker_client, config)
