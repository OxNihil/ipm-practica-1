from setuptools import setup, find_packages

setup(
    name= 'p1 libs',
    version= '0.1.1',
    scripts= ['atspi_dump.py'],
    packages= find_packages(include=['p1', 'p1.*'])
)
