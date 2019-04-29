from go2pod.utils import run


class KubeClient:
    # pylint: disable=no-self-use

    def __init__(self):
        pass

    def create(self, yaml_path):
        cmdstr = 'kubectl create -f {}'.format(yaml_path)
        cmd = run(cmdstr)
        return cmd.ok

    def get(self, yaml_path):
        cmdstr = 'kubectl get -f {}'.format(yaml_path)
        cmd = run(cmdstr)
        return cmd.ok

    def delete(self, yaml_path):
        cmdstr = 'kubectl delete -f {}'.format(yaml_path)
        cmd = run(cmdstr)
        return cmd.ok
