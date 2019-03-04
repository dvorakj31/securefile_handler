from setuptools import setup, find_packages
from distutils.extension import Extension


with open('README.rst') as f:
    long_description = ''.join(f.readlines())


setup(
    name='securefile_handler',
    packages=find_packages(),
    version='0.1.2',
    description='Module for secure (re)moving files and folders with content',
    long_description=long_description,
    author='Jakub Dvořák',
    author_email='dvoraj84@fit.cvut.cz',
    license='MIT',
    url='https://github.com/dvorakj31/securefile_handler',
    keywords='python module secure file content remove shred move',
    ext_modules=[Extension("securefile_handler._erase_helpers", ["securefile_handler/_erase_helpers.c"])],
    setup_requires=["pytest-runner"],
    tests_require=['pytest'],
    package_dir={"securefile_handler": "securefile_handler"},
    py_modules=['securefile_handler'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    zip_safe=False,
)
