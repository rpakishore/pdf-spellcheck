import re
from functools import cached_property
from typing import Any, Literal

import fitz


class Pdf:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    @cached_property
    def __doc(self):
        return fitz.open(stream=self.pdf_file.read(), filetype="pdf")

    def highlight(
        self,
        words_to_highlight: list[
            dict[Literal["original", "cleaned", "pages", "locations"], Any]
        ],
    ):
        """Generate PDF with highlighted words"""
        doc = self.__doc

        for entry in words_to_highlight:
            for location in entry["locations"]:
                page = doc[location["page"]]
                annot = page.add_rect_annot(location["bbox"])
                # Convert hex #57b431 to RGB (87, 180, 49)
                annot.set_colors(
                    fill=(87 / 255, 180 / 255, 49 / 255)
                )  # Using the green color
                annot.update(opacity=0.3)  # Semi-transparent

        return doc.tobytes()

    def process_pdf(
        self, dictionary: set[str]
    ) -> list[
        dict[
            tuple[str, str],
            dict[Literal["original", "cleaned", "pages", "locations"], Any],
        ]
    ]:
        """Process PDF and return misspelled words with locations"""
        doc = self.__doc
        misspelled: dict[
            tuple[str, str],
            dict[Literal["original", "cleaned", "pages", "locations"], Any],
        ] = {}

        for page_num, page in enumerate(doc, start=1):
            words = page.get_text("words")
            for word_info in words:
                original_word = word_info[4]
                cleaned_word = clean_word(original_word)

                if not cleaned_word:
                    continue

                if cleaned_word not in dictionary:
                    key = (original_word.upper(), cleaned_word)
                    entry = {
                        "original": original_word,
                        "cleaned": cleaned_word,
                        "pages": [],
                        "locations": [],
                    }

                    if key not in misspelled:
                        misspelled[key] = entry

                    misspelled[key]["pages"].append(page_num)
                    misspelled[key]["locations"].append(
                        {
                            "page": page_num - 1,  # 0-based index for PyMuPDF
                            "bbox": fitz.Rect(word_info[:4]),
                        }
                    )

        return list(misspelled.values())


def clean_word(word):
    """Clean and normalize words according to PRD rules"""
    # First remove all non-alphanumeric characters except hyphens
    cleaned = re.sub(r"[^A-Za-z0-9-]", "", word)
    # Convert to uppercase
    cleaned = cleaned.upper()
    # Remove hyphens
    cleaned = cleaned.replace("-", "")
    # Check for numbers
    if any(c.isdigit() for c in cleaned):
        return None
    return cleaned if cleaned else None
