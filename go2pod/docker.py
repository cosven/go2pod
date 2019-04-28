import delegator

from go2pod.utils import echo


class DockerClient:
    """Docker engine API client

    We call docker daemon remote api through docker command line tool
    since we know that the target user should have installed it and
    our use cases are pretty simple currently. No configurations needs
    to be done.

    In the long term, our use case will become more complicated,
    the `docker-py`_ library maybe be a better choice later.

    .. docker-py: https://github.com/docker/docker-py
    """

    def __init__(self, has_msb_support=False, need_sudo=False):
        """

        :param has_msb_support: has multi stage build support
        """
        self.need_sudo = need_sudo
        self.has_msb_support = has_msb_support

    def build(self, path, image=None):
        cmdstr = 'build {}'.format(path)
        if image is not None:
            cmdstr += ' -t {}'.format(image)
        cmdstr = self._decorate_cmd(cmdstr)
        cmd = delegator.run(cmdstr)
        if cmd.out:
            echo(cmd.out)
        if cmd.err:
            echo(cmd.err)
        return cmd.ok

    def _decorate_cmd(self, cmdstr):
        if self.need_sudo:
            return 'sudo docker ' + cmdstr
        else:
            return 'docker ' + cmdstr
