"""
This module defines functions for safe file erasing.
Algorithm for erasing is defined by British HMG Infosec Standard 5, Enhanced Standard.
Algorithm pseudocode:
    Open file
    In first round rewrite all bytes to zeros
    In second round rewrite all bytes to ones
    In third round rewrite all bytes to random values
"""
from pathlib import Path
import os
import sys
from ._erase_helpers import shred_file


def shred(filepath: Path):
    """
    Function, that securely shreds file.

    File operation exceptions are not handled.
    :param filepath: Path class with filepath
    """
    shred_file(bytes(Path(filepath.absolute())), filepath.stat().st_size)


def remove_dirtree(dirpath: Path, erase_function=shred):
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
    dirpath.rmdir()
