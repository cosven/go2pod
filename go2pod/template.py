def gen_dockerfile(config):
    dockerfile = []
    import_path = config.import_path
    workdir = '/go/src/' + import_path
    dockerfile.append('FROM {}'.format(config.base_image))
    for env_key, env_value in config.build_env.items():
        dockerfile.append('ENV {} {}'.format(env_key, env_value))
    dockerfile.append('RUN apk add --no-cache git wget')
    dockerfile.append('RUN {}'.format('go get {}'.format(import_path)))
    dockerfile.append('WORKDIR {}'.format(workdir))
    commands = config.build_commands
    dockerfile.append('RUN {}'.format(' && '.join(commands)))
    dockerfile.append('')
    return '\n'.join(dockerfile)


def gen_pod_yaml():
    """
    use jinja2 maybe?
    """
