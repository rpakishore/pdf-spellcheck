from pathlib import Path

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
    contents: list[str] = filepath.read_text(encoding="utf-8").splitlines()
    dictionary: set[str] = set([x.strip().upper() for x in contents])
    return dictionary
