from modeltestsdk.utils import make_serializable, to_snake_case, to_camel_case, from_datetime_string, format_class_name
import numpy as np
import pytest
from datetime import datetime, timedelta
from uuid import UUID


def test_make_serializable():
    assert make_serializable([
        [1, 2, 3],
        UUID('4175bd27-62e5-46ad-bbce-2f37c131bdb6'),
        np.array([1, 2, 3]),
        datetime(2020, 1, 1, 12, 32, 12, 32),
        timedelta(days=1),
        {'a': 1, 'b': 2, 'c': 3},
        {'dct': {'a': 1, 'b': 2, 'c': 3}}
    ]) == [
               [1, 2, 3],
               '4175bd27-62e5-46ad-bbce-2f37c131bdb6',
               [1, 2, 3],
               '2020-01-01T12:32:12.000032',
               86400.,
               {'a': 1, 'b': 2, 'c': 3},
               {'dct': {'a': 1, 'b': 2, 'c': 3}}
           ]

    assert make_serializable({'test': 'ok'}) == {'test': 'ok'}

    with pytest.raises(NotImplementedError) as e:
        make_serializable({'error': np.array([[1, 2, 3], [3, 2, 1]])})

    assert e.value.args[0] == "Unable to JSON serialize multidimensional ndarrays. Key = 'error'."

    with pytest.raises(NotImplementedError) as e:
        make_serializable(pytest)

    assert e.value.args[0] == f"Unable to convert object of type '{type(pytest)}' to JSON serializable."


def test_to_snake_case():
    assert to_snake_case('test') == 'test'
    assert to_snake_case('Test') == 'test'
    assert to_snake_case('TestTest') == 'test_test'
    assert to_snake_case([['Test_Test'], ['Test']]) == [['test_test'], ['test']]
    assert to_snake_case({'Test': 'TestTestTestTest'}) == {'test': 'test_test_test_test'}
    assert to_snake_case({'Test': ['TestTest', 'TestTest']}) == {'test': ['test_test', 'test_test']}


def test_to_camel_case():
    assert to_camel_case('test') == 'test'
    assert to_camel_case('Test') == 'test'
    assert to_camel_case('Test_Test') == 'testTest'
    assert to_camel_case([['Test_Test'], ['Test_Test']]) == [['testTest'], ['testTest']]
    assert to_camel_case({'Test_': 'Test_Test_Test'}) == {'test': 'testTestTest'}
    assert to_camel_case({'Test_': ['Test', 'Test_Test']}) == {'test': ['test', 'testTest']}


def test_from_datetime_string():
    assert from_datetime_string('2020-01-01T00:00:00') == datetime(2020, 1, 1, 0, 0, 0)
    assert from_datetime_string("2020-05-01T00:00:00Z").isoformat() == '2020-05-01T00:00:00+00:00'


def test_format_class_name():
    assert format_class_name('TestAPI') == 'test'
    assert format_class_name('TestTingAPI') == 'testting'
