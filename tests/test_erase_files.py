from pathlib import Path
import pytest
import preparements
import securefile_handler.securefile_handler
from securefile_handler.errors import WrongFilepathType, CannotBeShred, NotAFileError


def test_shred():
    fname = preparements.prepare_file()
    p = Path(fname)
    file_size = p.stat().st_size
    securefile_handler.securefile_handler.shred(Path(fname))
    assert p.exists()
    assert p.read_bytes() != preparements.TEST_TEXT
    assert p.stat().st_size == file_size
    preparements.delete_file(fname)


def test_shred_empty_file():
    fname = preparements.prepare_empty_file()
    p = Path(fname)
    assert p.exists()
    assert p.stat().st_size == 0
    securefile_handler.securefile_handler.shred(Path(fname))
    assert p.exists()
    assert p.stat().st_size == 0
    preparements.delete_file(fname)


def test_remove_file():
    fname = preparements.prepare_file()
    p = Path(fname)
    assert p.exists()
    assert p.stat().st_size > 0
    securefile_handler.securefile_handler.remove_file(fname)
    with pytest.raises(FileNotFoundError):
        assert p.stat()
    assert not p.exists()


def test_wrong_filepath_type_shred():
    with pytest.raises(WrongFilepathType):
        assert securefile_handler.securefile_handler.remove_file(10)
        assert securefile_handler.securefile_handler.remove_file(['some', 'bad', 'argument'])
        assert securefile_handler.securefile_handler.shred(['some', 'bad', 'argument'])
    with pytest.raises(CannotBeShred):
        tmp_dir = preparements.prepare_tmp_dir()
        assert securefile_handler.securefile_handler.shred(tmp_dir.name)
        tmp_dir.cleanup()
    with pytest.raises(NotAFileError):
        tmp_dir = preparements.prepare_tmp_dir()
        assert securefile_handler.securefile_handler.remove_file(tmp_dir.name)
        tmp_dir.cleanup()


def test_permission_error_shred():
    with pytest.raises(PermissionError):
        import os
        fname = preparements.prepare_file()
        default_mode = int(oct(os.stat(fname).st_mode & 0o777), 8)
        os.chmod(fname, 0)
        assert securefile_handler.securefile_handler.shred(fname)
    os.chmod(fname, default_mode)
    preparements.delete_file(fname)


def test_remove_dirtree():
    # TODO
    ...


