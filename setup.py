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
        'topopy'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': [
            'regulus=regulus.main:main',
            'morse=regulus.morse.main:run',
            'info=regulus.info:info',
            'resample = regulus.resample.resample_cli:resample_cli',
            'model = regulus.update.update_model_cli:update_model_cli',
            'refine = regulus.update.refine_topo_cli:refine_topo_cli',
            'recompute = regulus.update.recompute_topo_cli:recompute_topo_cli',

        ],
    }
)
