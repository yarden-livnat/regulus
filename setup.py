#!/usr/bin/env python

from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


with open('LICENSE') as f:
    license = f.read()

setup(
    name='regulus',
    version='0.1.0',
    description='Regulus',
    long_description=readme(),
    author='Yarden Livnat',
    author_email='yarden@sci.utah.edu',
    url='https://github.com/yarden_livnat/regulus.py',
    license=license,
    zip_safe=False,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[

    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points = {
        'console_scripts': [
            'regulus=regulus.main:main',
            'morse=regulus.morse.main:run',
            'info=regulus.info:info',
        ],
    }
)