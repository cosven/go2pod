from go2pod.utils import run


class KubeClient:
    def __init__(self):
        pass

    def apply_yaml(self, filepath):
        # pylint: disable=no-self-use
        cmdstr = 'kubectl apply -f {}'.format(filepath)
        cmd = run(cmdstr)
        return cmd.ok
