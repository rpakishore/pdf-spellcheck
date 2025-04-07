# /// script
# requires-python = ">=3.13"
# dependencies = [
#      "pymupdf>=1.25.3",
#      "streamlit>=1.42.2",
# ]
# ///

import csv
import pickle
import re
import tempfile
from functools import cached_property
from pathlib import Path

import fitz  # PyMuPDF
import pandas as pd
import streamlit as st


@st.cache_data
def load_dictionaries(dict_files: list[Path]) -> set[str]:
    """Load dictionary files into a set of lowercase words"""
    dictionary = set()
    for file in dict_files:
        _dict_vals = load_dictionary(filepath=file)
        dictionary.update(_dict_vals)
    return dictionary


def load_dictionary(filepath: Path) -> set[str]:
    pkl_file = filepath.with_suffix(".pkl")
    if pkl_file.exists() and pkl_file.is_file():
        with open(pkl_file, "rb") as f:
            return pickle.load(f)
    else:
        contents: list[str] = filepath.read_text(encoding="utf-8").splitlines()
        dictionary: set[str] = set([x.strip().upper() for x in contents])

        with open(pkl_file, "wb") as f:
            pickle.dump(dictionary, f, protocol=pickle.HIGHEST_PROTOCOL)
        return dictionary


def clean_word(word):
    """Clean and normalize words according to PRD rules"""
    # Remove all non-alphanumeric characters except hyphens
    cleaned = re.sub(r"[^A-Z0-9-]", "", word.upper())
    # Remove leading/trailing hyphens
    cleaned = cleaned.strip("-")
    # Check for digits
    if any(c.isdigit() for c in cleaned):
        return None
    return cleaned if cleaned else None


def process_pdf(pdf_file, dictionary):
    """Process PDF and return misspelled words with locations"""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    misspelled = {}

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


class Pdf:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    @cached_property
    def __doc(self):
        return fitz.open(stream=self.pdf_file.read(), filetype="pdf")

    def highlight(self, words_to_highlight):
        """Generate PDF with highlighted words"""
        doc = self.__doc

        for entry in words_to_highlight:
            for location in entry["locations"]:
                page = doc[location["page"]]
                annot = page.add_rect_annot(location["bbox"])
                annot.set_colors(fill=(1, 1, 0))  # Yellow fill
                annot.update(opacity=0.3)  # Semi-transparent

        return doc.tobytes()

    def process_pdf(self, dictionary):
        """Process PDF and return misspelled words with locations"""
        doc = self.__doc
        misspelled = {}

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


st.title("PDF Spell Checker")

pdf_file = st.file_uploader("Upload PDF", type=["pdf"])

if not pdf_file:
    misspelled_words = {}
    st.stop()

pdf = Pdf(pdf_file=pdf_file)

avl_dict_files: list[Path] = list(
    (Path(__file__).parent / "default_dict").glob("*.txt")
)

chosen_dicts = st.multiselect(
    label="Loaded Dictionaries",
    options=[file.stem for file in avl_dict_files],
    default=[file.stem for file in avl_dict_files],
)

dict_files = [
    (Path(__file__).parent / "default_dict" / f"{x}.txt") for x in chosen_dicts
]


if dict_files:
    with st.spinner("Processing..."):
        dictionary = load_dictionaries(dict_files)
        st.caption(f"*Dictionary loaded with {len(dictionary)} words*")

        misspelled_words = pdf.process_pdf(dictionary=dictionary)

        # Reset selections
        selected_words = set()
else:
    st.stop()

st.divider()

# Display results
if misspelled_words:
    st.subheader(f"Misspelled Words - *{len(misspelled_words)}* words found.")

    df_data = {
        "Include": [False for _ in range(len(misspelled_words))],
        "MisspelledWord": [x["original"] for x in misspelled_words],
        "Instances": [len(x["pages"]) for x in misspelled_words],
        "Pages": [
            ", ".join(map(str, sorted(set(x["pages"])))) for x in misspelled_words
        ],
    }
    df = pd.DataFrame(df_data)
    user_df = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Include": st.column_config.CheckboxColumn(
                "Include?",
                help="Include results in export",
                default=False,
                width="small",
            ),
            "MisspelledWord": st.column_config.TextColumn(
                "Misspelled Word", width="large"
            ),
            "Instances": st.column_config.NumberColumn("Instances", width="small"),
        },
    )

    st.divider()

    if chosen_words := [
        misspelled_words[_idx] for _idx in user_df[user_df["Include"]].index
    ]:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Export to CSV"):
                csv_data = []
                for entry in chosen_words:
                    csv_data.append(
                        {
                            "Word": entry["original"],
                            "Occurrences": len(entry["pages"]),
                            "Pages": ", ".join(map(str, sorted(set(entry["pages"])))),
                        }
                    )

                csv_file = tempfile.NamedTemporaryFile(delete=False)
                with open(csv_file.name, "w", newline="") as f:
                    writer = csv.DictWriter(
                        f, fieldnames=["Word", "Occurrences", "Pages"]
                    )
                    writer.writeheader()
                    writer.writerows(csv_data)

                st.download_button(
                    label="Download CSV",
                    data=open(csv_file.name, "rb").read(),
                    file_name="misspelled_words.csv",
                    mime="text/csv",
                )

        with col2:
            if st.button("Generate Highlighted PDF"):
                pdf_bytes = pdf.highlight(chosen_words)
                st.download_button(
                    label="Download Highlighted PDF",
                    data=pdf_bytes,
                    file_name="highlighted.pdf",
                    mime="application/pdf",
                )
else:
    st.info("No misspelled words found")
