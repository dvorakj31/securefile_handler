from securefile_handler.securefile_handler import _check_params
from pathlib import Path


def test_correct_params():
    assert _check_params(['some/path'])
    assert _check_params(['some/another_path'])
    assert _check_params([Path('some/path')])
    assert _check_params([Path('some/another_path')])


def test_bad_params():
    assert not _check_params([1])
    assert not _check_params([(1, 1)])
    assert not _check_params([{'1': 1}, 'second is correct'])
    assert not _check_params([[1, 2, 3]])
