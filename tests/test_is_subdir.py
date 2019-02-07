import pytest
from securefile_handler.errors import SameDirectoryError
from securefile_handler.securefile_handler import _is_subdir


def test_is_subdir():
    assert _is_subdir('/', '/home')
    assert _is_subdir('/source', '/source/dest')
    assert _is_subdir('/tmp/a/b/', '/tmp/a/b/c')
    assert _is_subdir('/root', '/root/some_subdir')


def test_is_subdir_error():
    with pytest.raises(SameDirectoryError):
        assert _is_subdir('/', '/')
        assert _is_subdir('~', '~')


def test_is_subdir_not():
    assert not _is_subdir('/home', '/')
    assert not _is_subdir('/a/b/c', '/a/b/')
    assert not _is_subdir('/a/b/c', '/a/b/d')
    assert not _is_subdir('/tmp', '/tmp2')
