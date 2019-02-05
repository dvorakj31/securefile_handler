from setuptools import setup, find_packages
from Cython.Build import cythonize


with open('README.rst') as f:
    long_description = ''.join(f.readlines())


setup(
    name='securefile_handler',
    packages=find_packages(),
    version='0.1',
    description='Module for secure (re)moving files and folders with content',
    long_description=long_description,
    author='Jakub Dvořák',
    author_email='dvoraj84@fit.cvut.cz',
    license='MIT',
    url='https://github.com/dvorakj31/securefile_handler',
    keywords='python module secure file content remove shred move',
    ext_modules=cythonize('securefile_handler/_erase_helpers.pyx'),
    setup_requires=[
        'Cython',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    tests_require=['pytest'],
    py_modules=['securefile_handler'],
    zip_safe=False,
)
