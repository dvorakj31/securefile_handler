"""
Helper file for preparing files to test.

Files are stored in folders for temporary files (e. g. for unix it's /tmp folder).

Files and folders are removed after testing.
"""


import tempfile
import os


TEST_TEXT = b'x' * 10


def prepare_file(directory=None):
    fd, fname = tempfile.mkstemp(dir=directory)
    os.write(fd, TEST_TEXT)
    os.close(fd)
    return fname


def prepare_empty_file():
    fd, fname = tempfile.mkstemp()
    os.close(fd)
    return fname


def delete_file(filename):
    os.remove(filename)


def prepare_tmp_dir(directory=None):
    return tempfile.TemporaryDirectory(dir=directory)


def prepare_dirtree(dir_number=3, file_number=10):
    tmp_dir = prepare_tmp_dir()
    for i in range(dir_number):
        new_dir = tmp_dir if not i else prepare_tmp_dir(tmp_dir.name)
        for _ in range(file_number):
            prepare_file(new_dir.name)
    return tmp_dir
