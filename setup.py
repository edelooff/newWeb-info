"""newWeb-info installer."""

import os
import re
from setuptools import setup, find_packages

REQUIREMENTS = [
    'newweb',
]


def readme():
  with file(os.path.join(os.path.dirname(__file__), 'README.md')) as r_file:
    return r_file.read()


def version():
  main_lib = os.path.join(os.path.dirname(__file__), 'newweb_info', 'pages.py')
  with file(main_lib) as v_file:
    return re.match(".*__version__ = '(.*?)'", v_file.read(), re.S).group(1)


setup(
    name='newweb_info',
    version=version(),
    description='An newWeb application to showcase newWeb.',
    long_description=readme(),
    classifiers=[
        "Programming Language :: Python",
        "Framework :: newWeb",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"],
    dependency_links=[
        'https://github.com/edelooff/newWeb/tarball/master#egg=newweb-dev',],
    author='Elmer de Looff',
    author_email='elmer.delooff@gmail.com',
    url='https://github.com/edelooff/newWeb-info',
    keywords='web newweb',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS)
