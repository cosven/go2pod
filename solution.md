方案草稿
------------

## 问题拆分

- [x] 配置文件设计？
  - 有的 go 项目构建时需要开启 `GO111MODULE` 特性，这或许是一个构建参数？
  - go get 太慢了？可以根据实际情况看是否支持 proxy 选项？

- [x] 一个 golang 项目构建的一般步骤？
  - 由于依赖下载可能被墙，`go build` 失败概率会挺高。

- [x] 怎样用这个镜像跑一个 pod？

## 一种思路

配置文件

```yaml
#
# http://go2pod.readthedocs.io
#
version: 1.0
url: https://github.com/OWNER/NAME

base_image: golang:1.12.4-alpine

# name: hello-world
# image: registry-host:port/{name}:latest-go2pod

build:
    env:
        GO111MODULE: auto
    commands:
        - go build

# Pod configuration
#
# we will always add a container "{name}-go2pod" to this pod.
#
# pod:
#     apiVersion: v1
#     kind: Pod
#     metadata:
#         name: {name}-go2pod
```
