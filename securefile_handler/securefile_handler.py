from . import _error
from . import _erase_helpers
from pathlib import Path
import os


def _check_params(params: list):
    for param in params:
        if not isinstance(param, (str, Path)):
            return False
    return True


def file_remove(filepath: (str, Path)):
    """
    Function, that removes securely file specified in parameter.

    File operation exceptions are not handled.
    :param filepath: Path to file specified with Path class or string.
    """
    if not _check_params([filepath]):
        raise _error.WrongFilepathType(f'Wrong filepath type {type(filepath)}')
    fpath = Path(filepath)
    if not fpath.is_file():
        raise _error.NotAFileError(f'Filepath is not a file {filepath}')
    _erase_helpers._shred(fpath)
    os.remove(fpath.absolute())


def shred(filepath: (str, Path)):
    """
    :param filepath: Path to file specified with Path class or string.
    """
    if not _check_params([filepath]):
        raise _error.WrongFilepathType(f'Wrong filepath type {type(filepath)}')
    fpath = Path(filepath)
    if not fpath.is_file() and not fpath.is_block_device():
        raise _error.CannotBeShred(f'This file cannot be shred {filepath}')
    _erase_helpers._shred(fpath)
