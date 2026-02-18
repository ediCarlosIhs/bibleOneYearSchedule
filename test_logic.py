from logic import get_column_dict, get_key
import pytest

def test_get_key():
    date = {"begin_date": "2026-02-17"}

    result = get_key(date)

    assert result == "begin_date"

def test_get_column_dict():
    mock_bible_column = {
        "gen": {
            "1": False,
            "2": False,
            "3": False,
            "4": False
        }
    }

    result = get_column_dict(mock_bible_column, "gen", "1", "3")

    assert "gen" in result

# Call the main function that is part of pytest so that the
# computer will execute the test functions in this file.
pytest.main(["-v", "--tb=line", "-rN", __file__])