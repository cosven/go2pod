import argparse
import textwrap

from colorama import init

from go2pod.cmds import (
    run_init,
    run_prepare,
    run_build,
    run_deploy,
    run_all_,
)
from go2pod.ensure import ensure_prerequisites
from go2pod.patch import patch_delegator


init()
patch_delegator()


def setup_argparse():
    parser = argparse.ArgumentParser(
        description=textwrap.dedent('''\
        go2pod - build GitHub golang project and deploy it on K8s.
        '''),
        formatter_class=argparse.RawTextHelpFormatter,
        prog='go2pod')
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s 0.1')
    subparsers = parser.add_subparsers(dest='cmd')
    subparsers.add_parser('init', description='create go2pod.yml template')
    subparsers.add_parser('prepare',
                          description='prepare Dockerfile and pod.yml')
    subparsers.add_parser('build', description='build docker image')
    subparsers.add_parser('deploy', description='deploy image on K8s')
    return parser


def main():
    parser = setup_argparse()
    args = parser.parse_args()

    if args.cmd is not None:
        if args.cmd == 'init':
            run_init()
            return

    try:
        ensure_prerequisites()
        if args.cmd == 'prepare':
            run_prepare()
        elif args.cmd == 'build':
            run_build()
        elif args.cmd == 'deploy':
            run_deploy()
        else:
            run_all_()
    except KeyboardInterrupt:
        raise SystemExit('exit.')
