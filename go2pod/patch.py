import delegator
from go2pod.utils import echo


def patch_delegator():
    old_run = delegator.run

    def delegator_run(command, *args, **kwargs):
        echo('> ' + command)
        return old_run(command, *args, **kwargs)

    delegator.run = delegator_run
