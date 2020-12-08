from setuptools import setup
from DomoticzAPI import version

setup(
    author='Xorfor',
    author_email='xorfor@hotmail.com',
    description='Domoticz API for Python',
    license='MIT License',
    name='DomoticzAPI',
    packages=['DomoticzAPI'],
    python_requires='>3',
    url='https://github.com/wini83/Domoticz-API/',
    version=version()
)
