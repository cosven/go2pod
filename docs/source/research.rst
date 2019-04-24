调研
==========

Go 项目是怎样构建的？
------------------------------
`Go 官方文档`_ 有这样一句话：

    Go程序的编译应当无需配置，或者除必要的导入语句外，不让开发者再做额外的事情。

看起来 ``go build`` 是个通用的编译命令。

不过看 Kubernetes 似乎是用 bazel 来构建的？


go build 的产物是什么？
----------------------------

好像和 c 有点像，如果检测到 main 函数的话，会生成一个二进制可执行文件。
二进制名字和当前目录名一样， `elvish`_ 项目是个不错的示例。

怎样构建 TiDB？
---------------------------------------

1. 先 clone (git clone 时会特别慢)
2. 运行 ``go build tidb-server/main.go`` 会报错，未安装依赖？

    **go.mod 文件是个啥？**

    参考文档 https://github.com/golang/go/wiki/Modules#quick-start ,
    再参考 TiDB 项目 makefile 可知，应该打开 `GO111MODULE` 特性。

3. 使用 ``GO111MODULE=on go build tidb-server/main.go``

bazel
--------------

    a fast, scalable, multi-language and extensible build system

看起来是个通用构建工具，所以先不管它。


.. _Go 官方文档: https://go-zh.org/doc/articles/go_command.html
.. _elvish: https://github.com/elves/elvish
