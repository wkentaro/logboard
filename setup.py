from __future__ import print_function

import distutils
import shlex
import subprocess
import sys

from setuptools import find_packages
from setuptools import setup


version = '0.4.0.post1'


if sys.argv[1] == 'release':
    if not distutils.spawn.find_executable('twine'):
        print(
            'Please install twine:\n\n\tpip install twine\n',
            file=sys.stderr,
        )
        sys.exit(1)

    commands = [
        'git pull origin master',
        'git tag v{:s}'.format(version),
        'git push origin master --tag',
        'python setup.py sdist',
        'twine upload dist/logboard-{:s}.tar.gz'.format(version),
    ]
    for cmd in commands:
        subprocess.check_call(shlex.split(cmd))
    sys.exit(0)


def get_long_description():
    with open('README.md') as f:
        long_description = f.read()

    try:
        import github2pypi
        return github2pypi.replace_url(
            slug='wkentaro/logboard', content=long_description
        )
    except Exception:
        return long_description


setup(
    name='logboard',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['flask', 'pandas', 'tabulate'],
    author='Kentaro Wada',
    author_email='www.kentaro.wada@gmail.com',
    description='Monitor and Compare Logs on Browser.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='http://github.com/wkentaro/logboard',
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
    entry_points={
        'console_scripts': [
            'logboard=logboard.cli.logboard:main',
            'logtable=logboard.cli.logtable:main',
        ],
    },
)
