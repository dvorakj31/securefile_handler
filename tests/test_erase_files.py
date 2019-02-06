from pathlib import Path
import pytest
import preparements
import securefile_handler.securefile_handler
from securefile_handler.errors import WrongFilepathType, CannotBeShred, NotAFileError, EmptyFolderError,\
    CannotReadFileError
import os


def test_shred():
    test_text = b'x' * 10
    fname = preparements.prepare_file(test_text)
    p = Path(fname)
    file_size = p.stat().st_size
    assert securefile_handler.securefile_handler.shred(Path(fname)) is None
    assert p.exists()
    assert p.read_bytes() != test_text
    assert p.stat().st_size == file_size
    preparements.delete_file(fname)


def test_shred_empty_file():
    fname = preparements.prepare_empty_file()
    p = Path(fname)
    assert p.exists()
    assert p.stat().st_size == 0
    assert securefile_handler.securefile_handler.shred(p) is None
    assert p.exists()
    assert p.stat().st_size == 0
    preparements.delete_file(fname)


def test_remove_file():
    test_text = b'x' * 10
    fname = preparements.prepare_file(test_text)
    p = Path(fname)
    assert p.exists()
    assert p.stat().st_size > 0
    assert securefile_handler.securefile_handler.remove_file(p) is None
    with pytest.raises(FileNotFoundError):
        p.stat()
    assert not p.exists()


def test_wrong_filepath_type_shred():
    with pytest.raises(WrongFilepathType):
        securefile_handler.securefile_handler.remove_file(10)
    with pytest.raises(WrongFilepathType):
        securefile_handler.securefile_handler.remove_file(('some', ))
    with pytest.raises(WrongFilepathType):
        securefile_handler.securefile_handler.shred(['some', 'bad', 'argument'])
    with pytest.raises(CannotBeShred):
        tmp_dir = preparements.prepare_tmp_dir()
        securefile_handler.securefile_handler.shred(tmp_dir)
    os.rmdir(tmp_dir)
    with pytest.raises(NotAFileError):
        tmp_dir = preparements.prepare_tmp_dir()
        securefile_handler.securefile_handler.remove_file(tmp_dir)
    os.rmdir(tmp_dir)


def test_permission_error_shred():
    with pytest.raises((CannotReadFileError, PermissionError)):
        test_text = b'some text'
        fname = preparements.prepare_file(test_text)
        default_mode = int(oct(os.stat(fname).st_mode & 0o777), 8)
        os.chmod(fname, 0)
        securefile_handler.securefile_handler.shred(fname)
    os.chmod(fname, default_mode)
    preparements.delete_file(fname)


def test_remove_dirtree():
    test_text = b'test text'
    directory_name = preparements.prepare_dirtree(test_text)
    dir_path = Path(directory_name)
    assert dir_path.exists()
    with pytest.raises(WrongFilepathType):
        securefile_handler.remove_dirtree((directory_name, ))
    securefile_handler.remove_dirtree(dir_path)
    assert not dir_path.exists()


def test_remove_empty_folder():
    directory_name = preparements.prepare_tmp_dir()
    with pytest.raises(EmptyFolderError):
        securefile_handler.remove_dirtree(directory_name)
    assert Path(directory_name).exists()
    os.rmdir(directory_name)


def test_remove_huge_files():
    file_list = []
    for i in range(10):
        file_list.append(preparements.prepare_file(test_text=b'x' * 100 * 1024 * 1024))
    for file in file_list:
        assert securefile_handler.remove_file(file) is None


def test_shred_huge_files():
    file_list = []
    for i in range(10):
        file_list.append(preparements.prepare_file(test_text=b'x' * 100 * 1024 * 1024))
    for file in file_list:
        assert securefile_handler.shred(file) is None
        assert Path(file).stat().st_size == 100 * 1024 * 1024
        os.remove(file)
