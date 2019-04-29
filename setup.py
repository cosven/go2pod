#!/usr/bin/env python3

from setuptools import setup


setup(
    name='go2pod',
    version='0.1',
    description='golang project to kubernetes pod',
    author='Cosven',
    author_email='yinshaowen241@gmail.com',
    packages=['go2pod', 'go2pod.cmds'],
    package_data={'': ['templates/*.template']},
    url='https://github.com/cosven/go2pod',
    keywords=['golang', 'kubernetes', 'pod'],
    classifiers=(
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        ),
    install_requires=[
        'colorama>=0.4',
        # it seems that delegator may have api breakchange in future version,
        # so we set the highest version here.
        'delegator.py<0.2',
        'pyyaml>=5.1',
        'jsonschema>=3.0.1',
    ],
    extras_require={},
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                "go2pod=go2pod.cli:main",
            ]
        },
    )
