import os

from go2pod.action import Action
from go2pod.const import PODYAML, VERSIONFILE
from go2pod.ensure import (
    ensure_config,
    ensure_tmpdir,
)
from go2pod.template import gen_dockerfile, gen_pod_yaml


def save_dockerfile(config, tmpdir):
    with Action('Saving dockerfile').start():
        dockerfile_path = os.path.join(tmpdir, 'Dockerfile')
        with open(dockerfile_path, 'w') as f:
            f.write(gen_dockerfile(config))
    return dockerfile_path


def save_pod_yaml(config, tmpdir):
    with Action('Saving pod yaml').start():
        pod_yaml_path = os.path.join(tmpdir, PODYAML)
        with open(pod_yaml_path, 'w') as f:
            f.write(gen_pod_yaml(config))
    return pod_yaml_path


def save_versionfile(config, tmpdir):
    with Action('Saving version info').start():
        versionfile_path = os.path.join(tmpdir, VERSIONFILE)
        with open(versionfile_path, 'w') as f:
            f.write(config.version)
    return versionfile_path


def run():
    config = ensure_config()
    tmpdir = ensure_tmpdir()
    save_dockerfile(config, tmpdir)
    save_pod_yaml(config, tmpdir)
    save_versionfile(config, tmpdir)
