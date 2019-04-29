import os


TEMPLATES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'templates'
)
POD_YAML_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'pod.yaml.template')


def gen_dockerfile(config):
    dockerfile = []
    git_info = config.git_info
    workdir_parent = '/go/src/{}/{}'.format(
        git_info['host'], git_info['namespace'])
    workdir = workdir_parent + '/{}'.format(git_info['name'])
    dockerfile.append('FROM {}'.format(config.base_image))
    for env_key, env_value in config.build_env.items():
        dockerfile.append('ENV {} {}'.format(env_key, env_value))
    dockerfile.append('RUN apk add --no-cache git wget')
    dumb_init_url = 'https://github.com/Yelp/dumb-init/'\
                    'releases/download/v1.2.2/dumb-init_1.2.2_amd64'
    dockerfile.append('RUN wget -q -O /dumb-init {} && chmod +x /dumb-init'
                      .format(dumb_init_url))
    dockerfile.append('RUN mkdir -p {}'.format(workdir_parent))
    zip_dirpath = '{}/{}'.format(workdir_parent, git_info['zip_dirname'])
    git_dirpath = '{}/{}'.format(workdir_parent, git_info['name'])
    dockerfile.append('RUN cd {workdir_parent} && '
                      'wget -q {zip_url} -O go2pod-project.zip && '
                      'unzip -q go2pod-project.zip && '
                      'rm go2pod-project.zip && '
                      'mv {zip_dirpath} {git_dirpath}'
                      .format(workdir_parent=workdir_parent,
                              zip_url=git_info['zip_url'],
                              zip_dirpath=zip_dirpath,
                              git_dirpath=git_dirpath))
    dockerfile.append('WORKDIR {}'.format(workdir))
    commands = config.build_commands
    dockerfile.append('RUN {}'.format(' && '.join(commands)))
    dockerfile.append('CMD ["/dumb-init", "tail", "-f", "/dev/null"]')
    dockerfile.append('')
    return '\n'.join(dockerfile)


def gen_pod_yaml(config):
    """
    use jinja2 maybe?
    """
    ctx = {'name': config.name,
           'image': config.image}
    with open(POD_YAML_TEMPLATE_PATH) as f:
        content = f.read()
    return content.format(**ctx)
