# go2pod

[![Documentation Status](https://readthedocs.org/projects/go2pod/badge/?version=latest)](https://go2pod.readthedocs.io/en/latest/?badge=latest)

go2pod is a command line tool that can build GitHub golang project
and deploy it on Kubernete.

For more information, refer to [the documentation](https://go2pod.readthedocs.io).

## Install

go2pod is published on PyPI and can be installed from there:

```
pip3 install go2pod
```

## Usage

```sh
go2pod init  # this will create go2pod.yml

# edit the go2pod.yml

go2pod       # build docker image and create pod
```

If you want to customize the build or deploy process, you can
run go2pod command step by step.

```sh
# build the docker image and create the pod.yml
go2pod build

# edit the pod.yml and run deploy command
go2pod deploy
```
