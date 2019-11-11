import os
from setuptools import setup, find_packages

req_pkgs = [line.rstrip() for line in open(os.path.join(os.path.dirname(__file__), 'install_requires.txt'), 'r')]

setup(
    name='fakerdb',
    version='1.0.0',
    packages=find_packages(),
    author='Daniel Maksimovich',
    author_email='maksimovich.daniel@gmail.com',
    description='Automatically generate data and fill your database tables with large volumes of test data.',
    keywords='data, generate, database, schema, relational',
    install_requires=req_pkgs
)
