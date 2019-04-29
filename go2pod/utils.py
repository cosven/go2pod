import delegator


__all__ = (
    'echo',
)


# output something to soem file or stdout
echo = print


def run(*args, **kwargs):
    kwargs['block'] = True
    cmd = delegator.run(*args, **kwargs)
    if cmd.out:
        echo(cmd.out, end='')
    if cmd.err:
        echo(cmd.err, end='')
    return cmd
