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
        cmd = self._run(cmdstr)
        return cmd.ok

    def push(self, image):
        cmdstr = 'push {}'.format(image)
        return self._run(cmdstr).ok

    def _run(self, cmdstr):
        cmdstr = self._decorate_cmd(cmdstr)
        cmd = delegator.run(cmdstr, block=False, timeout=None)
        while 1:
            out = cmd.subprocess.readline()
            if out:
                echo(out, end='')
            else:
                break
        cmd.block()
        return cmd

    def _decorate_cmd(self, cmdstr):
        if self.need_sudo:
            return 'sudo docker ' + cmdstr
        return 'docker ' + cmdstr
