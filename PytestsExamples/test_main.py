import pytest


class TestClass:

    def test_add_numbers_success(self):
        assert add_numbers(2, 3) == 5

    def test_add_numbers_fail(self):
        assert (add_numbers(2, 3) == 6) is False

    def test_index_error(self):
        with pytest.raises(AttributeError):  # Test purposefully fails to for educational purposes.
            raise_index_error()


def add_numbers(x: int, y: int):
    return x + y


def raise_index_error():
    raise IndexError()


def subtract_numbers(x: int, y: int):
    return x - y


def test_subtract_numbers():
    assert subtract_numbers(3, 2) == 1
