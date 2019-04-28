import delegator


__all__ = (
    'echo',
)


# output something to soem file or stdout
echo = print


def run(*args, **kwargs):
    cmd = delegator.run(*args, **kwargs)
    if cmd.out:
        echo(cmd.out)
    if cmd.err:
        echo(cmd.err)
    return cmd
