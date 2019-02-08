"""
Helper file for preparing files to test.

Files are stored in folders for temporary files (e. g. for unix it's /tmp folder).

Files and folders are removed after testing.
"""


import tempfile
import os
import shutil


def prepare_file(test_text, directory=None):
    fd, fname = tempfile.mkstemp(dir=directory)
    os.write(fd, test_text)
    os.close(fd)
    return fname


def prepare_empty_file():
    fd, fname = tempfile.mkstemp()
    os.close(fd)
    return fname


def delete_file(filename):
    os.remove(filename)


def delete_dirtree(root_dir):
    shutil.rmtree(root_dir)


def prepare_tmp_dir(directory=None):
    return tempfile.mkdtemp(dir=directory)


def prepare_dirtree(test_text, dir_number=3, file_number=10):
    tmp_dirname = prepare_tmp_dir()
    for i in range(dir_number):
        new_dir = tmp_dirname if not i else prepare_tmp_dir(tmp_dirname)
        for _ in range(file_number):
            prepare_file(test_text, new_dir)
    return tmp_dirname
