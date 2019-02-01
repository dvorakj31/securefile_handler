from pathlib import Path
import pytest
import _preparements
import securefile_handler.securefile_handler
from securefile_handler._error import WrongFilepathType, CannotBeShred, NotAFileError


def test_shred():
    fname = _preparements._prepare_file()
    p = Path(fname)
    file_size = p.stat().st_size
    securefile_handler.securefile_handler.shred(Path(fname))
    assert p.exists()
    assert p.read_bytes() != _preparements.TEST_TEXT
    assert p.stat().st_size == file_size
    _preparements._delete_file(fname)


def test_shred_empty_file():
    fname = _preparements._prepare_empty_file()
    p = Path(fname)
    assert p.exists()
    assert p.stat().st_size == 0
    securefile_handler.securefile_handler.shred(Path(fname))
    assert p.exists()
    assert p.stat().st_size == 0


def test_remove_file():
    fname = _preparements._prepare_file()
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
        tmp_dir = _preparements._prepare_tmp_dir()
        assert securefile_handler.securefile_handler.shred(tmp_dir.name)
        tmp_dir.cleanup()
    with pytest.raises(NotAFileError):
        tmp_dir = _preparements._prepare_tmp_dir()
        assert securefile_handler.securefile_handler.remove_file(tmp_dir.name)
        tmp_dir.cleanup()
