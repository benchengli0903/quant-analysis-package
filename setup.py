from setuptools import setup

from my_pip_package import __version__

setup(
    name='my_pip_package',
    version=__version__,

    url='https://github.com/benchengli0903/quant-analysis-package',
    author='Bencheng Li',
    author_email='libencheng191@gmail.com',

    py_modules=['my_pip_package'],
)
