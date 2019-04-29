import os

from go2pod.action import Action
from go2pod.const import CONFIG_YAML
from go2pod.template import gen_config_template
from go2pod.utils import echo


def create_config_template():
    if os.path.exists(CONFIG_YAML):
        echo('{} already exists.'.format(CONFIG_YAML))
        return
    with Action('Creating config template').start():
        with open(CONFIG_YAML, 'w') as f:
            f.write(gen_config_template())
        echo('{} is created.'.format(CONFIG_YAML))


def run():
    create_config_template()
