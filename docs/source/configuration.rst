自定义 go2pod.yml 配置
========================

url
-------
url 可以是一个 GitHub 项目地址，可以是一个项目某个分支、tag 的地址，
也可以项目在某一个 commit 时对应的地址。

举个例子：

.. code::

   url: https://github.com/elves/elvish
   url: https://github.com/pingcap/tidb/tree/v3.0.0-beta.1
   url: https://github.com/elves/elvish/tree/d1421bbe60c33d8b8c96a6717cbfc3916bffced3

.. _config-name:

name
----------------

name 代指项目名，它在镜像名和 pod 名都会有用到。默认情况下，
我们取 GitHub 项目的 REPO 名字做为项目名。

举个例子：

.. code::

   name: hello-world
   name: hi


base_image
---------------

base_image 为项目构建的基础镜像，目前只对 alpine 镜像进行了支持。
默认值为 ``golang:1.12.4-alpine`` 。

举个例子：

.. code::

   base_image: golang:1.12.4-alpine


apk
---------------

apk 指的 apline apk 包管理工具。我们目前支持给项目配置包依赖，
可以考虑支持指定 apk 源等。

举个例子，如果项目构建时依赖 make 和 gcc 包，我们可以这样配置：

.. code::

   apk:
     packages:
       - make
       - gcc


image
------------
项目构建完成后，会产生一个 Docker 镜像， image 字段指定的是这个镜像的名字。
它的默认值是 ``{name}:{version}-go2pod`` 。其中 ``{name}`` 和 ``{version}``
均是变量，我们会自动将它替换成对应的值。

其中变量 ``{name}`` 是指项目名 :ref:`config-name` 。 变量 ``version``
指项目构建的版本，详情可以参考 :ref:`thinking-version` 。

当我们需要使用私有镜像仓库时，我们应该配置这个字段。举个例子，
假如我们的私有镜像仓库地址为 ``localhost:5000`` ，可以这样配置：

.. code::

   image: localhost:5000/{name}:{version}-go2pod


build
-------------

我们可以设置构建时候的环境变量和构建命令。默认情况下，
构建命令为 ``go build`` 。

举个例子：

.. code::

   build:
     env:
       GO111MODULE: on

     commands:
       - go build server/main.go
