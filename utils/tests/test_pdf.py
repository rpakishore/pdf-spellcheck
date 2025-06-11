import io
from unittest.mock import MagicMock, patch

import pytest

from utils.pdf import Pdf, clean_word


@pytest.mark.parametrize(
    "input_word,expected",
    [
        ("Hello", "HELLO"),
        ("Hello-World", "HELLOWORLD"),
        ("Hello123", None),  # Words with numbers should return None
        ("Hello-World!", "HELLOWORLD"),
        ("", None),
        ("   ", None),
        ("123", None),
        ("Hello-World-", "HELLOWORLD"),
    ],
)
def test_clean_word(input_word, expected):
    assert clean_word(input_word) == expected


@pytest.fixture
def pdf_instance():
    mock_pdf_file = io.BytesIO(b"mock pdf content")
    return Pdf(mock_pdf_file)


@patch("fitz.open")
def test_highlight(mock_fitz_open, pdf_instance):
    # Mock the PDF document and its methods
    mock_doc = MagicMock()
    mock_page = MagicMock()
    mock_annot = MagicMock()
    mock_fitz_open.return_value = mock_doc
    mock_doc.__getitem__.return_value = mock_page
    mock_page.add_rect_annot.return_value = mock_annot

    # Test data
    words_to_highlight = [{"locations": [{"page": 0, "bbox": (100, 100, 200, 200)}]}]

    # Call the highlight method
    _ = pdf_instance.highlight(words_to_highlight)

    # Verify the interactions
    mock_doc.__getitem__.assert_called_once_with(0)
    mock_page.add_rect_annot.assert_called_once_with((100, 100, 200, 200))
    mock_annot.set_colors.assert_called_once()
    mock_annot.update.assert_called_once_with(opacity=0.3)
    mock_doc.tobytes.assert_called_once()


@patch("fitz.open")
def test_process_pdf(mock_fitz_open, pdf_instance):
    # Mock the PDF document and its methods
    mock_doc = MagicMock()
    mock_page = MagicMock()
    mock_fitz_open.return_value = mock_doc
    mock_doc.__iter__.return_value = [mock_page]

    # Mock page.get_text to return some test words
    mock_page.get_text.return_value = [
        (
            100,
            100,
            200,
            200,
            "Hello",
            0,
            0,
            0,
        ),  # (x0, y0, x1, y1, text, block_no, line_no, word_no)
        (300, 300, 400, 400, "World", 0, 0, 1),
    ]

    # Test dictionary
    dictionary = {"WORLD"}

    # Call process_pdf
    result = pdf_instance.process_pdf(dictionary)

    # Verify the results
    assert len(result) == 1  # Only "Hello" should be misspelled
    assert result[0]["original"] == "Hello"
    assert result[0]["cleaned"] == "HELLO"
    assert result[0]["pages"] == [1]
