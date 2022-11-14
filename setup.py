from setuptools import find_packages, setup
with open("README.md", "r", encoding="utf-8") as fh: long_description = fh.read()
with open("requirements.txt", encoding="utf-8") as fh: requirements = fh.read()
import pathlib


setup(
    name='logging_api',
    version='0.1.1',
    description='Test logging',
    url='https://github.com/JulioRomeroTorres/test-repo',
    author='Julio ',
    author_email='jcromerot@uni.pe',
    python_requires='>=3.8.0',
    license='MIT',
    packages=find_packages(include=["loggig_api", "loggig_api.*"]),
    install_requires=requirements
)
