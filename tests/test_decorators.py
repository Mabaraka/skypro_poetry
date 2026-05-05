import pytest

from src.decorators import log


def test_log_successful(capsys):
    @log()
    def foo(a, b):
        return a + b

    result = foo(1, 2)
    captured = capsys.readouterr()

    assert result == 3
    assert foo.__name__ == "foo"
    assert captured.out == "foo ok"


@pytest.mark.parametrize("args,kwargs", [((1, 2), {}), ((), {"a": 1, "b": 2})])
def test_log_failed(args, kwargs, capsys):
    @log()
    def foo(a, b):
        raise Exception("foo")

    with pytest.raises(Exception) as e:
        foo(*args, **kwargs)
    captured = capsys.readouterr()

    assert foo.__name__ == "foo"
    assert captured.out == f"foo error: {e.value}. Inputs: {args}, {kwargs}"


def test_log_successful_with_filename(tmp_path):
    log_file = tmp_path / "my_log.txt"

    @log(str(log_file))
    def foo(a, b):
        return a + b

    foo(1, 2)

    assert foo.__name__ == "foo"
    assert log_file.exists()
    assert log_file.read_text() == "foo ok"


@pytest.mark.parametrize("args,kwargs", [((1, 2), {}), ((), {"a": 1, "b": 2})])
def test_log_failed_with_filename(args, kwargs, tmp_path):
    log_file = tmp_path / "my_log.txt"

    @log(str(log_file))
    def foo(a, b):
        raise Exception("foo")

    with pytest.raises(Exception) as e:
        foo(*args, **kwargs)

    assert foo.__name__ == "foo"
    assert log_file.exists()
    assert log_file.read_text() == f"foo error: {e.value}. Inputs: {args}, {kwargs}"


def test_log_invalid_path():
    invalid_path = "non_existent_folder/my_log.txt"

    @log(invalid_path)
    def foo(a, b):
        return a + b

    with pytest.raises(FileNotFoundError):
        foo(1, 2)
