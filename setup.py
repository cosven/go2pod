#!/usr/bin/env python3

from setuptools import setup


setup(
    name='go2pod',
    version='0.1.dev0',
    description='golang project to kubernetes pod',
    author='Cosven',
    author_email='yinshaowen241@gmail.com',
    packages=['go2pod'],
    package_data={},
    url='https://github.com/cosven/go2pod',
    keywords=['golang', 'kubernetes'],
    classifiers=(
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        ),
    install_requires=['colorama', 'delegator.py'],
    extras_require={},
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                "go2pod=go2pod.cli:main",
            ]
        },
    )
