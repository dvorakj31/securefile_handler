from . import _error
from . import _erase_helpers
from pathlib import Path
import os


def _check_params(params: list):
    """
    Function for checking parameters of functions
    :param params: List of parameters of function.
    :return: True if all parameters are OK. Else False
    """
    for param in params:
        if not isinstance(param, (str, Path)):
            return False
    return True


def remove_file(filepath: (str, Path), erase_function=_erase_helpers._shred):
    """
    Function that removes securely file specified in parameter.

    File operation exceptions are not handled.
    :param filepath: Path to file specified with Path class or string.
    :param erase_function: Function for erasing data in files.
    """
    if not _check_params([filepath]):
        raise _error.WrongFilepathType(f'Wrong filepath type {type(filepath)}')
    fpath = Path(filepath)
    if not fpath.is_file():
        raise _error.NotAFileError(f'{filepath} is not a file')
    if not callable(erase_function):
        raise _error.EraseFunctionError(f'Wrong erase function type {type(erase_function)}')
    erase_function(fpath)
    os.remove(fpath.absolute())


def remove_dirtree(dirpath: (str, Path), erase_function=_erase_helpers._shred):
    """
    Function to remove folder with its content securely.
    :param dirpath: Path to directory
    :param erase_function: Function for erasing data in files.
    """
    if not _check_params([dirpath]):
        raise _error.WrongFilepathType(f'Wrong dirpath type {type(dirpath)}')
    if not callable(erase_function):
        raise _error.EraseFunctionError(f'Wrong erase function type {type(erase_function)}')
    _erase_helpers._remove_dirtree(Path(dirpath), erase_function)


def move_folder(src_dir: (str, Path), dst_dir: (str, Path), erase_function=_erase_helpers._shred):
    ...


def move_file(src: (str, Path), dst: (str, Path), erase_function=_erase_helpers._shred):
    ...


def shred(filepath: (str, Path), erase_function=_erase_helpers._shred):
    """
    Function to shred file content.
    :param filepath: Path to file specified with Path class or string.
    :param erase_function: Function for erasing data in file.
    """
    if not _check_params([filepath]):
        raise _error.WrongFilepathType(f'Wrong filepath type {type(filepath)}')
    fpath = Path(filepath)
    if not fpath.is_file() and not fpath.is_block_device() and not fpath.is_symlink():
        raise _error.CannotBeShred(f'This file cannot be shred {filepath}')
    if not callable(erase_function):
        raise _error.EraseFunctionError(f'Wrong erase function type {type(erase_function)}')
    erase_function(fpath)
