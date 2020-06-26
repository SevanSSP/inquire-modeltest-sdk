'''
Test base resource
'''


def test_repr(new_base_resource):
    r = repr(new_base_resource)
    assert isinstance(r, str)


def test_str(new_base_resource):
    s = str(new_base_resource)
    assert isinstance(s, str)

