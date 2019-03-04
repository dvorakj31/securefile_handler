import pytest
from unittest.mock import MagicMock
from pathlib import Path
import os
import securefile_handler.securefile_handler
from securefile_handler import errors
import preparements


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
        fake_file = MagicMock(spec=Path, wraps=Path, **attrs)
        fake_file.__fspath__ = lambda: file_path.absolute()
        securefile_handler.securefile_handler.move_file(fake_file, file_path)
    preparements.delete_file(file_path)
    with pytest.raises(errors.NotAFileError):
        tmp_dir = Path(preparements.prepare_tmp_dir())
        attrs = {
            'stat.return_value': FakeStat(tmp_dir.stat().st_dev + 1),
            'resolve': lambda: os.urandom(10)
        }
        fake_file = MagicMock(spec=Path, wraps=Path, **attrs)
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
    src_file = Path(preparements.prepare_file(b'test text1'))
    dst_file = Path(preparements.prepare_empty_file())
    attrs = {
        'stat.return_value': FakeStat(dst_file.stat().st_dev + 1),
        'resolve': lambda: dst_file.resolve(),
        'absolute': lambda: dst_file.absolute()
    }
    fake_file = MagicMock(spec=Path, wraps=Path, **attrs)
    assert securefile_handler.securefile_handler.move_file(src_file, fake_file) is None
    assert not src_file.exists()
    assert dst_file.is_file()
    assert dst_file.read_bytes() == b'test text1'
    preparements.delete_file(dst_file.absolute())


def test_move_file_symlink():
    if os.name == 'nt':
        # Pass symlink test on Windows
        return
    src_file = Path(preparements.prepare_file(b'test text1'))
    dst_file = Path(preparements.prepare_empty_file())
    symlink_file = Path(str(dst_file.resolve()) + '_symlink')
    symlink_file.symlink_to(src_file)
    attrs = {
        'stat.return_value': FakeStat(dst_file.stat().st_dev + 1),
        'resolve': lambda: dst_file.resolve(),
        'absolute': lambda: dst_file.absolute()
    }
    fake_file = MagicMock(spec=Path, wraps=Path, **attrs)
    assert securefile_handler.securefile_handler.move_file(symlink_file, fake_file) is None
    assert not src_file.exists()
    assert dst_file.is_file()
    assert dst_file.read_bytes() == b'test text1'
    preparements.delete_file(dst_file.absolute())


def test_move_file_new():
    src_file = Path(preparements.prepare_file(b'test text1'))
    dst_file = Path(preparements.prepare_empty_file())
    dst_path = dst_file.resolve()
    dst_dev = dst_file.stat().st_dev
    preparements.delete_file(dst_path)
    attrs = {
        'stat.return_value': FakeStat(dst_dev + 1),
        'resolve': lambda: dst_path,
        'absolute': lambda: dst_path
    }
    fake_file = MagicMock(spec=Path, wraps=Path, **attrs)
    assert securefile_handler.securefile_handler.move_file(src_file, fake_file) is None
    assert not src_file.exists()
    assert dst_file.is_file()
    assert dst_file.read_bytes() == b'test text1'
    preparements.delete_file(dst_file.absolute())


def test_move_folder():
    src_dir = Path(preparements.prepare_dirtree(b'test text1'))
    dst_dir = Path(preparements.prepare_tmp_dir())
    dst_path = dst_dir.resolve()
    dst_dev = dst_dir.stat().st_dev
    dst_dir.rmdir()
    attrs = {
        'stat.return_value': FakeStat(dst_dev + 1),
        'resolve': lambda: dst_path,
        'absolute': lambda: dst_path,
        '__fspath__': lambda x: str(dst_path),
        '__repr__': lambda x: str(dst_path),
        '__str__': lambda x: str(dst_path)
    }
    fake_file = MagicMock(spec=Path, wraps=Path, **attrs)
    assert securefile_handler.securefile_handler.move_folder(src_dir, fake_file) is None
    assert not src_dir.exists()
    assert dst_dir.is_dir()
    assert dst_dir.exists()
    for root, _, file_names in os.walk(dst_dir.resolve()):
        for file_name in file_names:
            assert Path(os.path.join(root, file_name)).read_bytes() == b'test text1'
            preparements.delete_file(Path(os.path.join(root, file_name)))
    preparements.delete_dirtree(dst_dir)


def test_move_folder_symlink():
    if os.name == 'nt':
        # Pass symlink test on Windows
        return
    src_dir = Path(preparements.prepare_dirtree(b'test text1'))
    dst_dir = Path(preparements.prepare_tmp_dir())
    dst_path = dst_dir.resolve()
    dst_dev = dst_dir.stat().st_dev
    dst_dir.rmdir()
    symlink_dir = Path(str(dst_path) + '_symlink')
    symlink_dir.symlink_to(src_dir)
    attrs = {
        'stat.return_value': FakeStat(dst_dev + 1),
        'resolve': lambda: dst_dir.resolve(),
        'absolute': lambda: dst_dir.absolute()
    }
    fake_file = MagicMock(spec=Path, wraps=Path, **attrs)
    assert securefile_handler.securefile_handler.move_folder(symlink_dir, fake_file) is None
    assert not src_dir.exists()
    assert dst_dir.is_dir()
    for root, _, file_names in os.walk(dst_dir.resolve()):
        for file_name in file_names:
            assert Path(os.path.join(root, file_name)).read_bytes() == b'test text1'
            preparements.delete_file(Path(os.path.join(root, file_name)))
    preparements.delete_dirtree(dst_dir)
