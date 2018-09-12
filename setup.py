#!/usr/bin/env python

from setuptools import setup, find_packages
import os


def readme():
    with open('README.md') as f:
        return f.read()


with open('LICENSE') as f:
    license = f.read()


def get_property(prop, project):
    """
        Helper function for retrieving properties from a project's
        __init__.py file
        @In, prop, string representing the property to be retrieved
        @In, project, string representing the project from which we will
        retrieve the property
        @Out, string, the value of the found property
    """
    result = re.search(
        r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
        open(os.path.join(project, "__init__.py").read(),
    )
    return result.group(1)

VERSION = get_property("__version__", "regulus")

setup(
    name='regulus',
    version=VERSION,
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
