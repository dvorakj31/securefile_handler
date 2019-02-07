import pytest
from unittest.mock import MagicMock
from pathlib import Path
import os
import securefile_handler.securefile_handler
from securefile_handler import errors
import preparements


class FakePathObject:

    _parts = ''

    def stat(self):
        raise NotImplementedError()

    def absolute(self):
        raise NotImplementedError()

    def __fspath__(self):
        raise NotImplementedError()


class FakeStat:
    def __init__(self, st_dev):
        self.st_dev = st_dev


def test_move_file_errors():
    with pytest.raises(errors.WrongFilepathType):
        securefile_handler.securefile_handler.move_file((',', ), 'str')
    with pytest.raises(errors.EraseFunctionError):
        securefile_handler.securefile_handler.move_file('correct/src', 'correct/dst', 'non-callable')
    with pytest.raises(errors.SameDriveError):
        securefile_handler.securefile_handler.move_file('/', '/',)
    with pytest.raises(errors.SameFileError):
        file_path = Path(preparements.prepare_empty_file())
        attrs = {
            'stat.return_value': FakeStat(file_path.stat().st_dev + 1),
            'resolve': file_path.resolve
        }
        fake_file = MagicMock(spec=Path, wraps=FakePathObject, **attrs)
        fake_file.__fspath__ = lambda: file_path.absolute()
        securefile_handler.securefile_handler.move_file(fake_file, file_path)
    preparements.delete_file(file_path)
    with pytest.raises(errors.NotAFileError):
        tmp_dir = Path(preparements.prepare_tmp_dir())
        attrs = {
            'stat.return_value': FakeStat(tmp_dir.stat().st_dev + 1),
            'resolve': lambda: os.urandom(10)
        }
        fake_file = MagicMock(spec=Path, wraps=FakePathObject, **attrs)
        fake_file.__fspath__ = lambda: file_path.absolute()
        securefile_handler.securefile_handler.move_file(tmp_dir, fake_file)
    tmp_dir.rmdir()


def test_move_folder_errors():
    with pytest.raises(errors.WrongFilepathType):
        securefile_handler.securefile_handler.move_folder((',', ), 'str')
    with pytest.raises(errors.EraseFunctionError):
        securefile_handler.securefile_handler.move_folder('correct/src', 'correct/dst', 'non-callable')
    with pytest.raises(errors.EmptyFolderError):
        tmp_dir = Path(preparements.prepare_tmp_dir())
        securefile_handler.move_folder(tmp_dir, tmp_dir)
    tmp_dir.rmdir()
    with pytest.raises(errors.SameDirectoryError):
        securefile_handler.securefile_handler.move_folder('/', '/')
    with pytest.raises(errors.SubDirectoryError):
        tmp_dir = Path(preparements.prepare_tmp_dir())
        dst_dir = Path(preparements.prepare_tmp_dir(tmp_dir.resolve()))
        securefile_handler.securefile_handler.move_folder(tmp_dir, dst_dir)
    tmp = dst_dir
    with pytest.raises(errors.SameDriveError):
        dst_dir = Path(preparements.prepare_tmp_dir())
        securefile_handler.securefile_handler.move_folder(tmp_dir, dst_dir)
    tmp.rmdir()
    dst_dir.rmdir()
    tmp_dir.rmdir()


def test_move_file():
    ...


def test_move_folder():
    ...
