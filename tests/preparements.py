import tempfile
import os


TEST_TEXT = b'x' * 10


def prepare_file():
    filename = tempfile.mktemp()
    with open(filename, 'wb') as ifile:
        ifile.write(TEST_TEXT)
    return filename


def prepare_empty_file():
    filename = tempfile.mktemp()
    with open(filename, 'w+'):
        pass
    return filename


def delete_file(filename):
    os.remove(filename)


def prepare_tmp_dir():
    return tempfile.TemporaryDirectory()
