from PyPDF2 import PdfReader
import re
from ae_spellcheck.wordlist import WordList

class PDF:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.pdf = PdfReader(filepath)
        self.wordlist = WordList()
    
    def __repr__(self):
        return f"PDF({self.filepath})"
    
    @property
    def pages(self):
        return self.pdf.pages
    
    def check(self):
        for i, page in enumerate(self.pdf.pages):
            page_number = i + 1
            page_text = page.extract_text()
            text_tuple = tuple(re.findall(r"([A-Za-z-]{2,})", page_text))
            if text_tuple:
                yield page_number, [error for error in self.wordlist.find_errors(text_tuple)]


    def extract_pages(self):
        self.page_text = { k: v for k, v in enumerate([page.extract_text() for page in self.pdf.pages])}