"""
Helper file for preparing files to test.

Files are stored in folders for temporary files (e. g. for unix it's /tmp folder).

Files and folders are removed after testing.
"""


import tempfile
import os
import shutil

import pytest


@pytest.fixture
def temp_file(request, directory=None):
    fd, fname = tempfile.mkstemp(dir=directory)
    os.write(fd, request.param)
    yield fname
    os.close(fd)
    delete_file(fname)


@pytest.fixture
def temp_files(request, directory=None):
    file_list = []
    for _ in range(10):
        fd, fname = tempfile.mkstemp(dir=directory)
        os.write(fd, request.param)
        os.close(fd)
        file_list.append(fname)
    yield file_list
    for fname in file_list:
        delete_file(fname)


@pytest.fixture
def empty_file():
    fd, fname = tempfile.mkstemp()
    yield fname
    os.close(fd)
    delete_file(fname)


def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def delete_dirtree(root_dir):
    shutil.rmtree(root_dir)


@pytest.fixture
def tmp_dir(directory=None):
    return tempfile.mkdtemp(dir=directory)


@pytest.fixture
def non_empty_tmp_dir(directory=None):
    d = tempfile.mkdtemp(dir=directory)
    tempfile.mkstemp(dir=d)
    yield d
    delete_dirtree(d)


@pytest.fixture
def tmp_dirtree(request, dir_number=3, file_number=10):
    tmp_dirname = tempfile.mkdtemp()
    for i in range(dir_number):
        new_dir = tmp_dirname if not i else tempfile.mkdtemp(dir=tmp_dirname)
        for _ in range(file_number):
            fd, fname = tempfile.mkstemp(dir=new_dir)
            os.write(fd, request.param)
            os.close(fd)
    yield tmp_dirname
