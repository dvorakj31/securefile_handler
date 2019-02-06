import pytest
from securefile_handler.errors import SameDirectoryError
from securefile_handler.securefile_handler import _is_subdir


def test_is_subdir():
    assert _is_subdir('/', '/home')
    assert not _is_subdir('/home', '/')
    assert not _is_subdir('/a/b/c', '/a/b/')
    assert not _is_subdir('/a/b/c', '/a/b/')
    with pytest.raises(SameDirectoryError):
        assert _is_subdir('/', '/')
        assert _is_subdir('~', '~')
    assert not _is_subdir('/tmp', '/tmp2')
    assert _is_subdir('/source', '/source/dest')
