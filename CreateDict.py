# /// script
# requires-python = ">=3.13"
# dependencies = [
#      "pymupdf>=1.25.3",
#      "streamlit>=1.42.2",
# ]
# ///

# uv run --with pymupdf --with streamlit streamlit run CreateDict.py

from pathlib import Path

import pandas as pd
import streamlit as st

from utils.dictionary import load_dictionaries
from utils.html import CSS_STYLE, FOOTER
from utils.pdf import Pdf

st.markdown(CSS_STYLE, unsafe_allow_html=True)

st.markdown(FOOTER, unsafe_allow_html=True)


st.markdown(
    '<h1 class="main-header">PDF Dictionary Generator</h1>', unsafe_allow_html=True
)

st.markdown(
    """
    <p style='color: #64748B; font-size: 1.1rem; margin-bottom: 2rem;'>
        Use this tool to find and add new dictionary words from existing PDFs. Upload a PDF, review the misspelled words,
        and add valid words to your dictionary.
    </p>
""",
    unsafe_allow_html=True,
)

pdf_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"],
    help="Upload a PDF file to extract potential dictionary words",
)

if not pdf_file:
    st.info("Please upload a PDF file to begin processing")
    st.stop()

pdf: Pdf = Pdf(pdf_file=pdf_file)

st.markdown('<h2 class="sub-header">Dictionary Selection</h2>', unsafe_allow_html=True)
avl_dict_files: list[Path] = list(
    (Path(__file__).parent / "default_dict").glob("*.txt")
)

chosen_dicts = st.multiselect(
    label="Select Dictionaries",
    options=[file.stem for file in avl_dict_files],
    default=[file.stem for file in avl_dict_files],
    help="Choose which dictionaries to use for word checking",
)

dict_files = [
    (Path(__file__).parent / "default_dict" / f"{x}.txt") for x in chosen_dicts
]

if dict_files:
    with st.spinner("Processing..."):
        dictionary = load_dictionaries(dict_files)
        st.caption(f"*Dictionary loaded with {len(dictionary)} words*")

        misspelled_words = pdf.process_pdf(dictionary=dictionary)

        selected_words = set()
else:
    st.stop()

st.divider()

st.markdown(
    """
    <div class="stInfo">
        <strong>FAQ: How does word cleaning and dictionary matching work?</strong><br>
        <ul>
            <li>When processing your PDF, the tool <b>removes punctuation and symbols</b> (like brackets, commas, periods) and converts all words to <b>UPPERCASE</b> before checking against the dictionary.</li>
            <li>When you add a word to the dictionary, it is the <b>cleaned version</b> (without punctuation, in uppercase) that is saved. For example, adding <code>NBCC</code> will also cover <code>(NBCC)</code>, <code>NBCC,</code>, <code>nbcc</code>, etc.</li>
            <li>Abbreviations and units (like <code>MPa</code>) will be stored as <code>MPA</code> in the dictionary, and all case variations will be recognized.</li>
            <li>There is no need to add bracketed or punctuated versions separately—just add the cleaned word once.</li>
        </ul>
        <span class="stCaption">If you have questions, check the dictionary text file to see exactly what was added.</span>
    </div>
    """,
    unsafe_allow_html=True,
)

if misspelled_words:
    st.markdown(
        f'<h2 class="sub-header">Results - {len(misspelled_words)} Potential Words Found</h2>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style='color: #64748B; margin-bottom: 1rem;'>
            Review the words below and select those that should be added to your dictionary. 
            Words are shown in their original form and after cleaning.
        </p>
    """,
        unsafe_allow_html=True,
    )

    df_data = {
        "Include": [False for _ in range(len(misspelled_words))],
        "MisspelledWord": [x["original"] for x in misspelled_words],
        "Corrected": [x["cleaned"] for x in misspelled_words],
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
                help="Include word in dictionary update",
                default=False,
                width="small",
            ),
            "MisspelledWord": st.column_config.TextColumn(
                "Original Word",
                width="medium",
            ),
            "Corrected": st.column_config.TextColumn(
                "Cleaned Word",
                width="medium",
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
    selected = user_df[user_df["Include"]]["Corrected"].to_list()
    if not selected:
        st.info("Select words to add to the dictionary")
        st.stop()

    st.markdown(
        '<h3 style="color: #2563EB; margin: 1rem 0;">Update Dictionary</h3>',
        unsafe_allow_html=True,
    )
    dict_to_update = st.selectbox(
        "Select Dictionary to Update",
        options=[file.stem for file in avl_dict_files],
        help="Choose which dictionary to add the selected words to",
    )

    if st.button(
        "Update Dictionary", help="Add selected words to the chosen dictionary"
    ):
        with open(
            (Path(__file__).parent / "default_dict" / f"{dict_to_update}.txt"), "a"
        ) as f:
            f.write("\n" + "\n".join(sorted(selected)))
        st.success(f"Successfully added {len(selected)} words to {dict_to_update}")
        st.session_state.clear()
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()

else:
    st.info("✅ No potential new words found in the document")
