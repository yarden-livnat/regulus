#!/usr/bin/env python

from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


with open('LICENSE') as f:
    license = f.read()

setup(
    name='regulus',
    version='0.4.0',
    description='Regulus',
    long_description=readme(),
    author='Yarden Livnat',
    author_email='yarden@sci.utah.edu',
    url='https://github.com/yarden_livnat/regulus',
    license=license,
    zip_safe=False,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'topopy>=0.1', 'numpy', 'sklearn', 'pandas'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': [
        ],
    }
)
