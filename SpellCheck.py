# /// script
# requires-python = ">=3.13"
# dependencies = [
#      "pymupdf>=1.25.3",
#      "streamlit>=1.42.2",
# ]
# ///

import csv
import tempfile
from pathlib import Path
from typing import Any, Literal

import pandas as pd
import streamlit as st

from utils.dictionary import load_dictionaries
from utils.html import CSS_STYLE, FOOTER
from utils.pdf import Pdf

st.markdown(CSS_STYLE, unsafe_allow_html=True)

st.markdown(FOOTER, unsafe_allow_html=True)

st.markdown('<h1 class="main-header">PDF Spell Checker</h1>', unsafe_allow_html=True)
st.markdown(
    """
    <p style='color: #64748B; font-size: 1.1rem; margin-bottom: 2rem;'>
        Upload your PDF document to check for spelling errors. Select your preferred dictionaries 
        and export the results or generate a highlighted PDF.
    </p>
""",
    unsafe_allow_html=True,
)

pdf_file = st.file_uploader(
    "Upload PDF", type=["pdf"], help="Upload a PDF file to check for spelling errors"
)

if not pdf_file:
    st.info("Please upload a PDF file to begin spell checking")
    st.stop()

pdf: Pdf = Pdf(pdf_file=pdf_file)

st.markdown('<h2 class="sub-header">Dictionary Selection</h2>', unsafe_allow_html=True)
avl_dict_files: list[Path] = list(
    (Path(__file__).parent / "default_dict").glob("*.txt")
)

chosen_dicts: list[str] = st.multiselect(
    label="Select Dictionaries",
    options=[file.stem for file in avl_dict_files],
    default=[file.stem for file in avl_dict_files],
    help="Choose which dictionaries to use for spell checking",
)

dict_files: list[Path] = [
    (Path(__file__).parent / "default_dict" / f"{x}.txt") for x in chosen_dicts
]


if dict_files:
    with st.spinner("Processing..."):
        dictionary: set[str] = load_dictionaries(dict_files)
        st.caption(f"*Dictionary loaded with {len(dictionary)} words*")

        misspelled_words: list[
            dict[
                tuple[str, str],
                dict[Literal["original", "cleaned", "pages", "locations"], Any],
            ]
        ] = pdf.process_pdf(dictionary=dictionary)

        selected_words: set[str] = set()
else:
    st.stop()

st.divider()

if misspelled_words:
    st.markdown(
        f'<h2 class="sub-header">Results - {len(misspelled_words)} Misspelled Words Found</h2>',
        unsafe_allow_html=True,
    )

    df_data = {
        "Include": [False for _ in range(len(misspelled_words))],
        "MisspelledWord": [x["original"] for x in misspelled_words],
        "Instances": [len(x["pages"]) for x in misspelled_words],
        "Pages": [
            ", ".join(map(str, sorted(set(x["pages"])))) for x in misspelled_words
        ],
    }
    df = pd.DataFrame(df_data)

    st.markdown(
        """
        <p style='color: #64748B; margin-bottom: 1rem;'>
            Select the words you want to include in the export. You can then download the results as a CSV file 
            or generate a highlighted PDF.
        </p>
    """,
        unsafe_allow_html=True,
    )

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
                "Misspelled Word",
                width="large",
            ),
            "Instances": st.column_config.NumberColumn(
                "Instances",
                width="small",
            ),
            "Pages": st.column_config.TextColumn(
                "Pages",
                width="medium",
            ),
        },
    )

    st.divider()

    if chosen_words := [
        misspelled_words[_idx] for _idx in user_df[user_df["Include"]].index
    ]:
        st.markdown(
            '<h3 style="color: #2563EB; margin: 1rem 0;">Export Options</h3>',
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export to CSV", help="Download results as a CSV file"):
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
            if st.button(
                "📄 Generate Highlighted PDF",
                help="Generate a PDF with highlighted misspelled words",
            ):
                pdf_bytes = pdf.highlight(chosen_words)
                st.download_button(
                    label="Download Highlighted PDF",
                    data=pdf_bytes,
                    file_name="highlighted.pdf",
                    mime="application/pdf",
                )
else:
    st.info("✅ No misspelled words found in the document")
