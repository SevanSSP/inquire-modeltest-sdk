from modeltestSDK.utils import to_datetime_string, from_datetime_string


def test_datetime_strings():
    s = "2008-09-03T20:56:35.450686Z"
    assert s == to_datetime_string(from_datetime_string("2008-09-03T20:56:35.450686Z"))
    assert s == to_datetime_string(from_datetime_string("2008-09-03T20:56:35.450686+00:00"))