from server import add_list_of_numbers


def test_add_numbers():
    """Test basic number addition"""
    result = add_list_of_numbers([2, 2])

    expected = {
        "numbers": [2, 2],
        "sum": 4,
        "count": 2,
        "average": 2.0,
        "min": 2,
        "max": 2,
        "summary": "Sum of [2, 2] = 4",
    }

    assert result == expected
