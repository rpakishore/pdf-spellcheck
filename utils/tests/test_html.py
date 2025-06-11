import pytest

from utils.html import CSS_STYLE, FOOTER


@pytest.mark.parametrize(
    "style",
    [
        ".stApp",
        ".main-header",
        ".sub-header",
        ".stButton",
        ".stFileUploader",
        ".stDataEditor",
        ".footer",
        ".stDivider",
        ".stInfo",
        ".stCaption",
    ],
)
def test_css_style_content(style):
    assert style in CSS_STYLE


@pytest.mark.parametrize(
    "element",
    [
        'class="footer"',
        "Created and maintained by",
        "Arun Kishore",
        "Structural EIT",
        "Vancouver Office",
    ],
)
def test_footer_content(element):
    assert element in FOOTER


@pytest.mark.parametrize(
    "prop",
    ["color:", "font-size:", "margin:", "padding:", "background-color:", "border:"],
)
def test_css_style_formatting(prop):
    assert CSS_STYLE.startswith("<style>")
    assert CSS_STYLE.endswith("</style>")
    assert prop in CSS_STYLE


def test_footer_formatting():
    assert FOOTER.startswith('<div class="footer">')
    assert FOOTER.endswith("</div>")
    assert "href='mailto:" in FOOTER
    assert "</a>" in FOOTER
