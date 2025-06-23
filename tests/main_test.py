import asyncio

from server import add_list_of_numbers


def test_add_numbers():
    """Test basic number addition"""
    result = asyncio.run(add_list_of_numbers([2, 2]))
    assert result == "Sum of [2, 2] = 4"
