from pathlib import Path
import pytest
import securefile_handler.securefile_handler
from securefile_handler.errors import WrongFilepathType, CannotBeShred, NotAFileError, EmptyFolderError,\
    CannotReadFileError
import os


@pytest.mark.parametrize('temp_file', [b'test_text 1', b'test_text 2'], indirect=['temp_file'])
def test_shred(temp_file):
    test_text = b'x' * 10
    p = Path(temp_file)
    file_size = p.stat().st_size
    assert securefile_handler.securefile_handler.shred(Path(temp_file)) is None
    assert p.exists()
    assert p.read_bytes() != test_text
    assert p.stat().st_size == file_size


def test_shred_empty_file(empty_file):
    fname = empty_file
    p = Path(fname)
    assert p.exists()
    assert p.stat().st_size == 0
    assert securefile_handler.securefile_handler.shred(p) is None
    assert p.exists()
    assert p.stat().st_size == 0


@pytest.mark.parametrize('temp_file', [b'test_text 1'], indirect=['temp_file'])
def test_remove_file(temp_file):
    test_text = b'x' * 10
    fname = temp_file
    p = Path(fname)
    assert p.exists()
    assert p.stat().st_size > 0
    assert securefile_handler.securefile_handler.remove_file(p) is None
    with pytest.raises(FileNotFoundError):
        p.stat()
    assert not p.exists()


def test_wrong_filepath_type_shred(tmp_dir):
    with pytest.raises(WrongFilepathType):
        securefile_handler.securefile_handler.remove_file(10)
    with pytest.raises(WrongFilepathType):
        securefile_handler.securefile_handler.remove_file(('some', ))
    with pytest.raises(WrongFilepathType):
        securefile_handler.securefile_handler.shred(['some', 'bad', 'argument'])
    with pytest.raises(CannotBeShred):
        securefile_handler.securefile_handler.shred(tmp_dir)
    with pytest.raises(NotAFileError):
        securefile_handler.securefile_handler.remove_file(tmp_dir)


@pytest.mark.parametrize('temp_file', [b'test_text 1'], indirect=['temp_file'])
def test_permission_error_shred(temp_file):
    with pytest.raises((CannotReadFileError, PermissionError)):
        fname = temp_file
        default_mode = int(oct(os.stat(fname).st_mode & 0o777), 8)
        os.chmod(fname, 0)
        securefile_handler.securefile_handler.shred(fname)
    os.chmod(fname, default_mode)


@pytest.mark.parametrize('tmp_dirtree', [b'x' * 10], indirect=['tmp_dirtree'])
def test_remove_dirtree(tmp_dirtree):
    directory_name = tmp_dirtree
    dir_path = Path(directory_name)
    assert dir_path.exists()
    with pytest.raises(WrongFilepathType):
        securefile_handler.remove_dirtree((directory_name, ))
    securefile_handler.remove_dirtree(dir_path)
    assert not dir_path.exists()


def test_remove_empty_folder(tmp_dir):
    directory_name = tmp_dir
    with pytest.raises(EmptyFolderError):
        securefile_handler.remove_dirtree(directory_name)
    assert Path(directory_name).exists()


@pytest.mark.parametrize('temp_files', [b'x' * 10], indirect=['temp_files'])
def test_remove_huge_files(temp_files):
    for file in temp_files:
        assert securefile_handler.remove_file(file) is None


@pytest.mark.parametrize('temp_files', [b'x' * 10], indirect=['temp_files'])
def test_shred_huge_files(temp_files):
    for file in temp_files:
        assert securefile_handler.shred(file) is None
        assert Path(file).stat().st_size == 10
