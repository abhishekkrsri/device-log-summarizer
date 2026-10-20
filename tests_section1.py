"""Section 1 practice tests.

Complete clean_sensor_readings() in main.py yourself before running these tests.
These tests are provided as test expectations; the implementation is intentionally
left for you because the assessment says Section 1 must be done without AI.
"""
from main import clean_sensor_readings


def test_mixed_values():
    assert clean_sensor_readings([25, "30.5", None, -10, "invalid", 600, 45]) == [
        25.0, 30.5, 500.0, 45.0
    ]


def test_empty_list():
    assert clean_sensor_readings([]) == []


def test_all_invalid_values():
    assert clean_sensor_readings([None, "bad", -1, "-5"]) == []


if __name__ == "__main__":
    test_mixed_values()
    test_empty_list()
    test_all_invalid_values()
    print("All Section 1 tests passed.")
