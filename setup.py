from setuptools import setup, find_packages
from settings import PACKAGE_NAME

assert PACKAGE_NAME is not None, "Please give a package name in settings.py"
setup(name=PACKAGE_NAME,
      packages=find_packages())