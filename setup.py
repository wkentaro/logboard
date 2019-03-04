from __future__ import print_function

from setuptools import find_packages
from setuptools import setup


version = '0.1'


setup(
    name='chainerlg',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    author='Kentaro Wada',
    author_email='www.kentaro.wada@gmail.com',
    description='Chainer log browser.',
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
    entry_points={'console_scripts': ['chainerlg=chainerlg:main']},
)
