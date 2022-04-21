#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os

from setuptools import Command, find_packages, setup

NAME = "scrapy-redis-cluster"
FOLDER = "scrapy_redis_cluster"
DESCRIPTION = "Redis Cluster for Scrapy."
EMAIL = "jiaqi.code@outlook.com"
AUTHOR = "LJQ"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = '0.7.2'


def read_file(filename):
    with open(filename) as fp:
        return fp.read().strip()


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines() if not line.startswith("#")]


REQUIRED = read_requirements("requirements.txt")

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION
print(long_description)
about = {}
if not VERSION:
    with open(os.path.join(here, FOLDER, "__init__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    url='https://github.com/Jiaqi0109/scrapy-redis-cluster',
    project_urls={"Documentation": "https://github.com/Jiaqi0109/scrapy-redis-cluster"},
    packages=find_packages(),
    install_requires=REQUIRED,
    license="MIT",
    zip_safe=False,
    keywords=[
        'scrapy-redis',
        'scrapy-redis-cluster'
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
)