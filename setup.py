from setuptools import setup
import os
import os.path


def get_packages(top):
    packages = []
    for dirname, subdirs, filenames in os.walk(top):
        initpy = os.path.join(dirname, '__init__.py')
        is_python_package = os.path.isfile(initpy)
        if is_python_package:
            packages.append(dirname)
    return packages


setup(
    name='cq',
    version='0.13',
    url='https://github.com/lukaszb/cq',
    license='MIT',
    description='simple cqrs implementation',
    author='Lukasz Balcerzak',
    author_email='lukaszbalcerzak@gmail.com',
    zip_safe=False,
    packages=get_packages('cq'),
    include_package_data=True,
    install_requires=[
        'jsonfield',  # TODO: only needed django, make it optional
        'marshmallow>=2.13',
    ],
)
