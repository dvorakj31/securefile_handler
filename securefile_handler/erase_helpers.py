"""
This module defines functions for safe file erasing.
Algorithm for erasing is defined by British HMG Infosec Standard 5, Enhanced Standard.
Algorithm pseudocode:
    Open file
    In first round rewrite all bytes to zeros
    In secod round rewrite all bytes to ones
    In third round rewrite all bytes to random values
"""
from pathlib import Path
import os


def _shred_file(filepath: Path):
    """
    Function, that securely shreds file.

    File operation exceptions are not handled.
    :param filepath: Path class with filepath
    """
    file_size = filepath.stat().st_size
    with filepath.open('wb+') as input_file:
        for i in range(3):
            input_file.seek(0, 0)
            for _ in range(file_size):
                val = bytes([i]) if i < 2 else os.urandom(1)
                input_file.write(val)
            # Ensure, that bytes are written to file
            input_file.flush()


def file_remove(filepath: str):
    """
    Function, that removes securely file specified in parameter.

    File operation exceptions are not handled.
    :param filepath: path to file.
    """
    _shred_file(Path(filepath))
    os.remove(filepath)
