from contextlib import contextmanager

from colorama import Fore

from go2pod.utils import echo


class ActionError(Exception):
    pass


class ActionFailed(ActionError):
    pass


class ActionWarning(ActionError):
    pass


class Action:
    """an contextmanager used for logging progess and results

    start -> [fail|warn]
    """
    def __init__(self, desc):
        self.desc = desc

    @contextmanager
    def start(self):
        s = self.desc + '...\t'
        echo(s, flush=True)
        try:
            yield self
        except ActionWarning as e:
            echo(s + Fore.YELLOW + 'failed' + Fore.RESET)
        except ActionFailed as e:
            echo(s + Fore.RED + 'failed' + Fore.RESET)
            echo(Fore.RED + '\n\t' + str(e) + '\n', Fore.RESET)
            raise SystemExit('Prerequisites checking failed, exit.')
        except KeyboardInterrupt:
            echo(s + Fore.YELLOW + 'cancelled' + Fore.RESET)
            raise
        else:
            echo(s + Fore.GREEN + 'ok' + Fore.RESET)

    def fail(self, msg=''):
        # pylint: disable=no-self-use
        raise ActionFailed(msg)

    def warn(self, msg=''):
        # pylint: disable=no-self-use
        raise ActionWarning(msg)

    def ensure_true(self, condition, msg='', warn_only=False):
        """like assert, but raise ActionError instead when failed"""
        if not condition:
            if not warn_only:
                self.fail(msg)
            else:
                self.warn(msg)
