# go2pod

[![Documentation Status](https://readthedocs.org/projects/go2pod/badge/?version=latest)](https://go2pod.readthedocs.io/en/latest/?badge=latest)

go2pod is a command line tool that can build GitHub golang project
and deploy it on Kubernetes.

For more information, refer to [the documentation](https://go2pod.readthedocs.io).

## Install

go2pod is published on PyPI and can be installed from there:

```
pip3 install go2pod
```

## Quick Start

1. Create go2pod configuration file template

```sh
go2pod init
```

2. Edit the [go2pod.yml](https://go2pod.readthedocs.io/en/latest/configuration.html)

3. Build docker image and create kubernetes pod

```
go2pod
```

If you want to customize the build or deploy process, you can
run go2pod command step by step.

```sh
# prepare Dockerfile and pod.yml
go2pod prepare

# build the docker image
go2pod build

# edit the pod.yml and run deploy command
go2pod deploy
```
