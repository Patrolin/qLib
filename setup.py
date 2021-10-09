from setuptools import setup

setup(
    name='qLib',
    version='0.0',
    author='Patrolin',
    author_email='patrik@balas.cz',
    packages=['qLib', 'qLib.statistics'],
    scripts=['bin/script1', 'bin/script2'], # wat
    url='http://pypi.python.org/pypi/qLib',
    license='LICENSE.md',
    description='A library of tradeoffs',
    long_description=open('README.md').read(),
)
