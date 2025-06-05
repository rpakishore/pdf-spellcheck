# /// script
# requires-python = ">=3.13"
# dependencies = [
#      "pymupdf>=1.25.3",
#      "streamlit>=1.42.2",
# ]
# ///

# uv run --with pymupdf --with streamlit streamlit run CreateDict.py

import re
from functools import cached_property
from pathlib import Path

import fitz  # PyMuPDF
import pandas as pd
import streamlit as st

st.markdown("""
    <style>
    /* Global styles */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Typography */
    .main-header {
        color: #1E3A8A;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #1E3A8A;
    }
    
    .sub-header {
        color: #2563EB;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #2563EB;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #1E3A8A;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* File uploader styling */
    .stFileUploader {
        border: 2px dashed #2563EB;
        border-radius: 8px;
        padding: 2rem;
        background-color: #F8FAFC;
    }
    
    /* Data editor styling */
    .stDataEditor {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        background-color: #F8FAFC;
        color: #64748B;
        padding: 1rem;
        border-top: 1px solid #E2E8F0;
        font-size: 0.9rem;
    }
    
    .footer a {
        color: #2563EB;
        text-decoration: none;
        font-weight: 500;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    /* Divider styling */
    .stDivider {
        margin: 2rem 0;
        border-color: #E2E8F0;
    }
    
    /* Info message styling */
    .stInfo {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Caption styling */
    .stCaption {
        color: #64748B;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer">
        Created and maintained by <a href='mailto:remaa@ae.ca'>Arun Kishore</a> | 
        Structural EIT, Vancouver Office
    </div>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_dictionaries(dict_files: list[Path]) -> set[str]:
    """Load dictionary files into a set of lowercase words"""
    dictionary = set()
    for file in dict_files:
        _dict_vals = load_dictionary(filepath=file)
        dictionary.update(_dict_vals)
    return dictionary


def load_dictionary(filepath: Path) -> set[str]:
    contents: list[str] = filepath.read_text(encoding="utf-8").splitlines()
    dictionary: set[str] = set([x.strip().upper() for x in contents])
    return dictionary


def clean_word(word):
    """Clean and normalize words according to PRD rules"""
    cleaned = re.sub(r"[^A-Z0-9-]", "", word.upper())
    cleaned = cleaned.strip("-")
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


st.markdown('<h1 class="main-header">PDF Dictionary Generator</h1>', unsafe_allow_html=True)
st.markdown("""
    <p style='color: #64748B; font-size: 1.1rem; margin-bottom: 2rem;'>
        Use this tool to find and add new dictionary words from existing PDFs. Upload a PDF, review the misspelled words,
        and add valid words to your dictionary.
    </p>
""", unsafe_allow_html=True)

pdf_file = st.file_uploader("Upload PDF", type=["pdf"], help="Upload a PDF file to extract potential dictionary words")

if not pdf_file:
    st.info("Please upload a PDF file to begin processing")
    st.stop()

pdf = Pdf(pdf_file=pdf_file)

st.markdown('<h2 class="sub-header">Dictionary Selection</h2>', unsafe_allow_html=True)
avl_dict_files: list[Path] = list(
    (Path(__file__).parent / "default_dict").glob("*.txt")
)

chosen_dicts = st.multiselect(
    label="Select Dictionaries",
    options=[file.stem for file in avl_dict_files],
    default=[file.stem for file in avl_dict_files],
    help="Choose which dictionaries to use for word checking"
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

if misspelled_words:
    st.markdown(
        f'<h2 class="sub-header">Results - {len(misspelled_words)} Potential Words Found</h2>',
        unsafe_allow_html=True
    )

    st.markdown("""
        <p style='color: #64748B; margin-bottom: 1rem;'>
            Review the words below and select those that should be added to your dictionary. 
            Words are shown in their original form and after cleaning.
        </p>
    """, unsafe_allow_html=True)

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

    st.markdown('<h3 style="color: #2563EB; margin: 1rem 0;">Update Dictionary</h3>', unsafe_allow_html=True)
    dict_to_update = st.selectbox(
        "Select Dictionary to Update",
        options=[file.stem for file in avl_dict_files],
        help="Choose which dictionary to add the selected words to"
    )
    
    if st.button("Update Dictionary", help="Add selected words to the chosen dictionary"):
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
