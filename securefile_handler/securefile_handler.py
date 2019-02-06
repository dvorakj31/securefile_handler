from . import errors
from . import erase_helpers
from pathlib import Path
import os
import shutil


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


def _is_subdir(parent_path: str, child_path: str):
    """
    Function for checking if child_path is subdir of parent_path
    :param parent_path: Path string to parent folder
    :param child_path: Path string to child file
    :return: If folders are same exception SameDirectoryError will be raised else returns True or False depending on
    child path being subdir.
    """
    parent = Path(os.path.abspath(parent_path)).resolve()
    child = Path(os.path.abspath(child_path)).resolve()
    if parent == child:
        raise errors.SameDirectoryError(f'{parent_path} and {child} are the same folders')
    return parent in child.parents


def remove_file(filepath: (str, Path), erase_function=erase_helpers.shred):
    """
    Function that removes securely file specified in parameter.

    File operation exceptions are not handled.
    :param filepath: Path to file specified with Path class or string.
    :param erase_function: Function for erasing data in files.
    """
    if not _check_params([filepath]):
        raise errors.WrongFilepathType(f'Wrong filepath type {type(filepath)}')
    fpath = Path(filepath)
    if not fpath.is_file():
        raise errors.NotAFileError(f'{filepath} is not a file')
    if not callable(erase_function):
        raise errors.EraseFunctionError('Erase function is not callable')
    erase_function(fpath)
    os.remove(fpath.absolute())


def remove_dirtree(dirpath: (str, Path), erase_function=erase_helpers.shred):
    """
    Function to remove folder with its content securely.

    Folder must contain some files.

    :param dirpath: Path to non-empty directory
    :param erase_function: Function for erasing data in files.
    """
    if not _check_params([dirpath]):
        raise errors.WrongFilepathType(f'Wrong dirpath type {type(dirpath)}')
    if not callable(erase_function):
        raise errors.EraseFunctionError('Erase function is not callable')
    dir_path = Path(dirpath)
    if len(os.listdir(dir_path.absolute())) == 0:
        raise errors.EmptyFolderError(f'Folder {dir_path.absolute()} is empty')
    erase_helpers.remove_dirtree(dir_path, erase_function)


def move_folder(src_dir: (str, Path), dst_dir: (str, Path), erase_function=erase_helpers.shred):
    """
    Function that moves folder with its content to another device.

    This function will copy folder with content and then delete the old folder with content.
    :param src_dir: Source path of directory.
    :param dst_dir: Destination path of directory.
    :param erase_function: Function for erasing data in files.
    """
    if not _check_params([src_dir, dst_dir]):
        raise errors.WrongFilepathType(f'Wrong parameter type')
    if not callable(erase_function):
        raise errors.EraseFunctionError('Erase function is not callable')
    if _is_subdir(str(src_dir), str(dst_dir)):
        raise errors.SubDirectoryError(f'Cannot move {dst_dir} subdirectory of {src_dir}')
    src_path, dst_path = Path(src_dir), Path(dst_dir)
    if src_path.stat().st_dev == dst_path.stat().st_dev:
        raise errors.SameDriveError("Cannot move folder to same drive")
    if len(os.listdir(src_path.absolute())) == 0:
        raise errors.EmptyFolderError(f'Folder {src_path.absolute()} is empty')
    shutil.copytree(src_path.resolve(), dst_path.resolve())
    erase_helpers.remove_dirtree(src_path, erase_function)


def move_file(src: (str, Path), dst: (str, Path), erase_function=erase_helpers.shred):
    """
    Function that moves file to another device.

    Function copy file to another device and delete file on source path.
    :param src: Source path of file.
    :param dst: Destination path of file.
    :param erase_function: Function for erasing data in files. This optional argument is a callable.
    """
    if not _check_params([src, dst]):
        raise errors.WrongFilepathType(f'Wrong parameter type')
    if not callable(erase_function):
        raise errors.EraseFunctionError('Erase function is not callable')
    src_path, dst_path = Path(src), Path(dst)
    if src_path.stat().st_dev == dst_path.stat().st_dev:
        raise errors.SameDriveError("Cannot move file to same drive")
    if not src_path.is_file():
        raise errors.NotAFileError(f'{src} is not a regular file')
    shutil.copy2(src_path.absolute(), dst_path.absolute())
    erase_function(src_path)


def shred(filepath: (str, Path), erase_function=erase_helpers.shred):
    """
    Function to shred file content.
    :param filepath: Path to file specified with Path class or string.
    :param erase_function: Function for erasing data in file.
    """
    if not _check_params([filepath]):
        raise errors.WrongFilepathType(f'Wrong filepath type {type(filepath)}')
    fpath = Path(filepath)
    if not fpath.is_file() and not fpath.is_block_device() and not fpath.is_symlink():
        raise errors.CannotBeShred(f'This file cannot be shred {filepath}')
    if not callable(erase_function):
        raise errors.EraseFunctionError(f'Wrong erase function type {type(erase_function)}')
    erase_function(fpath)
