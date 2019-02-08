from pathlib import Path
import os
from ._erase_helpers import shred_file


def shred(filepath: Path, chunk_size=4 * 1024):
    """
    Function, that securely shreds file.

    File operation exceptions are not handled.

    :param filepath: Path class with filepath
    :param chunk_size: Size of chunk for amount of bytes rewritten at once. Consider changing this value.
    This may slow your device.
    """
    shred_file(bytes(Path(filepath.absolute())), filepath.stat().st_size, chunk_size)


def remove_dirtree(dirpath: Path, erase_function: callable = shred):
    """
    Function to help remove directory tree

    :param dirpath: Path to root directory specified with Path class
    :param erase_function: Function for erasing data in files.
    """
    directories, filepaths = [], []
    for root, dirs, fnames in os.walk(dirpath):
        for dir_name in dirs:
            directories.append(Path(os.path.join(root, dir_name)))
        for fname in fnames:
            filepaths.append(os.path.join(root, fname))
    for file in filepaths:
        erase_function(Path(file))
        os.remove(file)
    for directory in directories:
        directory.rmdir()
    os.rmdir(dirpath.resolve())
    if dirpath.is_symlink():
        os.remove(dirpath)
