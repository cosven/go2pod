from go2pod.cmds.build import (
    build_docker_image,
    push_docker_image,
)
from go2pod.cmds.deploy import create_or_update_pod
from go2pod.cmds.prepare import (
    save_pod_yaml,
    save_dockerfile,
    save_versionfile,
)
from go2pod.ensure import (
    ensure_config,
    ensure_docker,
    ensure_kube,
    ensure_tmpdir,
)


def run():
    config = ensure_config()
    kube_client = ensure_kube()
    docker_client = ensure_docker()
    tmpdir = ensure_tmpdir()

    save_dockerfile(config, tmpdir)
    pod_yaml_path = save_pod_yaml(config, tmpdir)
    save_versionfile(config, tmpdir)

    build_docker_image(docker_client, config, tmpdir)
    push_docker_image(docker_client, config)

    create_or_update_pod(kube_client, pod_yaml_path)
