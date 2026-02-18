from main import get_key

def test_get_key():

    mock_dict = {"begin_date": "2026-02-17", "other_key": "value"}

    result = get_key(mock_dict)

    assert result == "begin_date"