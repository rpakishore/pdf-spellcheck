from pathlib import Path
from unittest.mock import patch

from utils.dictionary import load_dictionaries, load_dictionary


def test_load_dictionary():
    # Test data
    mock_content = "word1\nword2\nWORD3\n"

    with patch("pathlib.Path.read_text", return_value=mock_content):
        result = load_dictionary(Path("dummy.txt"))

        # Verify results
        assert result == {"WORD1", "WORD2", "WORD3"}
        assert isinstance(result, set)


def test_load_dictionary_empty_file():
    with patch("pathlib.Path.read_text", return_value=""):
        result = load_dictionary(Path("empty.txt"))
        assert result == set()


def test_load_dictionary_with_whitespace():
    mock_content = "  word1  \n  word2  \n  WORD3  \n"

    with patch("pathlib.Path.read_text", return_value=mock_content):
        result = load_dictionary(Path("whitespace.txt"))
        assert result == {"WORD1", "WORD2", "WORD3"}


@patch("utils.dictionary.load_dictionary")
def test_load_dictionaries(mock_load_dictionary):
    # Mock the load_dictionary function to return different sets for different files
    mock_load_dictionary.side_effect = [{"WORD1", "WORD2"}, {"WORD3", "WORD4"}]

    dict_files = [Path("dict1.txt"), Path("dict2.txt")]
    result = load_dictionaries(dict_files)

    # Verify results
    assert result == {"WORD1", "WORD2", "WORD3", "WORD4"}
    assert mock_load_dictionary.call_count == 2

    # Verify the function was called with correct arguments
    mock_load_dictionary.assert_any_call(filepath=Path("dict1.txt"))
    mock_load_dictionary.assert_any_call(filepath=Path("dict2.txt"))
