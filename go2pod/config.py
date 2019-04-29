import re
import time

import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from go2pod.exc import Go2podException


schema = {
    'type': 'object',
    'properties': {
        'version': {'type': 'number'},
        'url': {'type': 'string'},
        'name': {'type': 'string'},
        'base_image': {'type': 'string'},
        'apk': {
            'type': 'object',
            'properties': {
                'packages': {'type': 'array'},
            }
        },
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


def _parse_github_url(url):
    url_regex = re.compile(
        r'(https?://)?(github.com/[\w\d_\.-]+/[\w\d_\.-]+)'
        r'(/tree/[\w\d_\.-]+)?'
    )
    m = url_regex.match(url)
    if m is None:
        raise ConfigLoadError('invalid github url')
    g1, g2, g3 = m.groups()
    g1 = g1 or 'https://'
    g3 = g3 or 'tree/master'
    git_commit = g3.split('/')[-1]
    zip_url = g1 + g2 + '/archive/' + git_commit + '.zip'
    git_host, git_namespace, git_name = g2.split('/')
    zip_dirname = '{}-{}'.format(git_name, git_commit)

    git_info = {
        'host': git_host,
        'namespace': git_namespace,
        'name': git_name,
        'commit': git_commit,
        'zip_url': zip_url,
        'zip_dirname': zip_dirname,
    }
    return git_info


class Config:

    def __init__(self, yml_data, version=None):
        self._yml_data = yml_data
        self._build = self._yml_data.get('build', {})
        self._apk = self._yml_data.get('apk', {})
        self.git_info = _parse_github_url(self.url)

        # If commit is a 40 digits sha-1 hash, we only use the
        # first 7 digits, which is enough for most projects
        # and the early git use only 7 hex digits for hash
        commit = self.git_info['commit']
        sha1_regex = re.compile(r'[0-9a-f]{40}')
        if sha1_regex.match(commit) is not None:
            self._version = commit[:7]
        else:
            if version is None:
                self._version = commit + '-' + str(int(time.time()))
            else:
                self._version = version

    @property
    def name(self):
        default = self.git_info['name']
        return self._yml_data.get('name', default)

    @property
    def url(self):
        return self._yml_data['url']

    @property
    def version(self):
        return self._version

    @property
    def base_image(self):
        default = 'golang:1.12.4-alpine'
        return self._yml_data.get('base_image', default)

    @property
    def apk_packages(self):
        return self._apk.get('packages', []) + ['wget', 'git']

    @property
    def build_env(self):
        return self._build.get('env', {})

    @property
    def build_commands(self):
        default = ['go build']
        return self._build.get('commands', default)

    @property
    def image(self):
        default = '{name}:{version}-go2pod'
        image_tpl = self._yml_data.get('image', default)
        image = image_tpl.format(name=self.name,
                                 version=self.version)
        return image

    @classmethod
    def load(cls, path, version=None):
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigLoadError('invalid yaml config file')

        # check config version, validate and deserialize
        try:
            validate(data, schema)
        except ValidationError as e:
            msg = "field '#/{}': {}".format('/'.join(e.path), e.message)
            raise ConfigLoadError(msg)
        return cls(data, version=version)
