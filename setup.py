from __future__ import print_function

import shlex
import subprocess

from setuptools import find_packages
from setuptools import setup


def githash():
    cmd = 'git log -1 --format="%h"'
    try:
        hash_ = subprocess.check_output(shlex.split(cmd)).decode().strip()
    except subprocess.CalledProcessError:
        hash_ = None
    return hash_


version = '0.1.0-0'


hash_ = githash()
if hash_ is not None:
    version = '%s.%s' % (version, hash_)


setup(
    name='logboard',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['flask', 'pandas'],
    author='Kentaro Wada',
    author_email='www.kentaro.wada@gmail.com',
    description='Monitor and Compare Logs on Browser.',
    url='http://github.com/wkentaro/chainer-logs',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    entry_points={'console_scripts': ['logboard=logboard.cli:main']},
)
