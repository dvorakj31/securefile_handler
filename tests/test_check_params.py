import securefile_handler.securefile_handler as handler_lib
from pathlib import Path


def test_correct_params():
    assert handler_lib._check_params(['some/path'])
    assert handler_lib._check_params(['some/another_path'])
    assert handler_lib._check_params([Path('some/path')])
    assert handler_lib._check_params([Path('some/another_path')])


def test_bad_params():
    assert not handler_lib._check_params([1])
    assert not handler_lib._check_params([(1, 1)])
    assert not handler_lib._check_params([{'1': 1}, 'second is correct'])
    assert not handler_lib._check_params([[1, 2, 3]])
