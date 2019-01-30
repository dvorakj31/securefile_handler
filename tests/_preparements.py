import tempfile
import os


TEST_TEXT = b'x' * 10


def _prepare_file():
    filename = tempfile.mktemp()
    with open(filename, 'wb') as ifile:
        ifile.write(TEST_TEXT)
    return filename


def _prepare_empty_file():
    filename = tempfile.mktemp()
    with open(filename, 'w+') as input_file:
        pass
    return filename


def _delete_file(filename):
    os.remove(filename)
