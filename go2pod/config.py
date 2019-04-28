import re
from urllib.parse import urlparse

import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from go2pod.exc import Go2podException


config_yaml_tmpl = """\
#
# http://go2pod.readthedocs.io
#
version: 1.0
url: https://github.com/OWNER/NAME

base_image: golang:1.12.4-alpine

# name: hello-world
# image: registry-host:port/{name}:latest-go2pod

build:
    env:
        GO111MODULE: auto
        HTTP_PROXY: http://172.17.0.1:8123
        HTTPS_PROXY: http://172.17.0.1:8123
    commands:
        - go build

# build artifacts
artifacts:
    - ./tidb-server/tidb-server

# Pod configuration
#
# we will always add a container "{name}-go2pod" to this pod.
#
# pod:
#     apiVersion: v1
#     kind: Pod
#     metadata:
#         name: {name}-go2pod
"""

schema = {
    'type': 'object',
    'properties': {
        'version': {'type': 'number'},
        'url': {'type': 'string'},
        'base_image': {'type': 'string'},
        'build': {
            'type': 'object',
            'properties': {
                'commands': {'type': 'array'},
                'env': {'type': 'object'}
            }
        }
    },
    'required': ['url', 'version'],
}


class ConfigLoadError(Go2podException):
    pass


class Config:

    def __init__(self, yml_data):
        self._yml_data = yml_data

        result = urlparse(self._yml_data['url'])
        self._import_path = result.netloc + result.path
        self._name = result.path.split('/')[-1]

    @property
    def name(self):
        return self._name

    @property
    def import_path(self):
        return self._import_path

    @property
    def url(self):
        return self._yml_data['url']

    @property
    def build(self):
        return self._yml_data.get('build', {})

    @property
    def base_image(self):
        return self._yml_data.get('base_image', 'golang:1.12.4-alpine')

    @property
    def build_env(self):
        return self.build.get('env', {})

    @property
    def build_commands(self):
        return self.build.get('commands', [])

    @property
    def image(self):
        tag = 'latest-go2pod'
        default = '{}:{}'.format(self.name, tag)
        return self._yml_data.get('image', default)

    @classmethod
    def load(cls, path):
        try:
            with open(path) as f:
                data = yaml.load(f, Loader=yaml.Loader)
        except yaml.YAMLError:
            raise ConfigLoadError('invalid yaml config file')

        # check config version, validate and deserialize
        try:
            validate(data, schema)
        except ValidationError as e:
            msg = "field '#/{}': {}".format('/'.join(e.path), e.message)
            raise ConfigLoadError(msg)
        cls.validate(data)
        return cls(data)

    @classmethod
    def validate(cls, data):
        cls.validate_url(data['url'])

    @classmethod
    def validate_url(cls, url):
        p = re.compile(r'(?:https?://)?github.com/[\w\d_\.-]+/[\w\d_\.-]+')
        if p.match(url) is None:
            raise ConfigLoadError('invalid github repo url')
