import securefile_handler.erase_helpers
import _preparements
import pytest
from pathlib import Path


def test_shred():
    fname = _preparements._prepare_file()
    p = Path(fname)
    file_size = p.stat().st_size
    securefile_handler.erase_helpers._shred_file(Path(fname))
    assert p.exists()
    assert p.read_bytes() != _preparements.TEST_TEXT
    assert p.stat().st_size == file_size
    _preparements._delete_file(fname)


def test_shred_empty_file():
    fname = _preparements._prepare_empty_file()
    p = Path(fname)
    assert p.exists()
    assert p.stat().st_size == 0
    securefile_handler.erase_helpers._shred_file(Path(fname))
    assert p.exists()
    assert p.stat().st_size == 0


def test_file_remove():
    fname = _preparements._prepare_file()
    p = Path(fname)
    assert p.exists()
    assert p.stat().st_size > 0
    securefile_handler.erase_helpers.file_remove(fname)
    with pytest.raises(FileNotFoundError):
        assert p.stat()
    assert not p.exists()
