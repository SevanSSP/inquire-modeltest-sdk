"""
Test base resource
"""


def test_floater_test_conversion(floater_test_data, tests_class, floater_test_class):
    floater_tests = tests_class.parse_obj([floater_test_class(**item) for item in floater_test_data])
    print(floater_tests)
    assert(floater_tests[0].wave_id == '9bcbe75a-d527-4aa8-ae98-b8a5c778db03')
