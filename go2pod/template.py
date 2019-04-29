import os


TEMPLATES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'templates'
)
POD_YAML_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'pod.yaml.template')
CONFIG_YAML_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'go2pod.yml.template')


def gen_dockerfile(config):
    dockerfile = []
    git_info = config.git_info
    workdir_parent = '/go/src/{}/{}'.format(
        git_info['host'], git_info['namespace'])
    workdir = workdir_parent + '/{}'.format(git_info['name'])
    dockerfile.append('FROM {}'.format(config.base_image))
    for env_key, env_value in config.build_env.items():
        dockerfile.append('ENV {} {}'.format(env_key, env_value))
    apk_packages = ' '.join(config.apk_packages)
    dockerfile.append('RUN apk add --no-cache {}'.format(apk_packages))
    dumb_init_url = 'http://github.com/Yelp/dumb-init/'\
                    'releases/download/v1.2.2/dumb-init_1.2.2_amd64'
    dockerfile.append('RUN wget -T 5 -O /dumb-init {} && chmod +x /dumb-init'
                      .format(dumb_init_url))
    dockerfile.append('RUN mkdir -p {}'.format(workdir_parent))
    zip_dirpath = '{}/{}'.format(workdir_parent, git_info['zip_dirname'])
    git_dirpath = '{}/{}'.format(workdir_parent, git_info['name'])
    zip_filename_tmp = '{}-{}.zip'.format(config.name, config.version)
    dockerfile.append('RUN cd {workdir_parent} && '
                      'wget {zip_url} -O {zip_filename_tmp} -T 5 && '
                      'unzip -q {zip_filename_tmp} && '
                      'rm {zip_filename_tmp} && '
                      'mv {zip_dirpath} {git_dirpath}'
                      .format(workdir_parent=workdir_parent,
                              zip_filename_tmp=zip_filename_tmp,
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


def gen_config_template():
    with open(CONFIG_YAML_TEMPLATE_PATH) as f:
        content = f.read()
    return content
