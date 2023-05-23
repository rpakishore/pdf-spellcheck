# importing required modules
from PyPDF2 import PdfReader
  
# creating a pdf reader object
reader = PdfReader(r"C:\Users\remaa\Desktop\Temp\prp_cov_shoring_structural_review_20230419_v2-Page_23 Copy_ocr.pdf")
  
# printing number of pages in pdf file
print(len(reader.pages))
  
# getting a specific page from the pdf file
page = reader.pages[0]
  
# extracting text from page
text = page.extract_text()
print(text)

class PDF:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.pdf = PdfReader(filepath)
    
    def __repr__(self):
        return f"PDF({self.filepath})"
    
    @property
    def pages(self):
        return self.pdf.pages
    
    def extract_pages(self):
        self.page_text = { k: v for k, v in enumerate([page.extract_text() for page in self.pdf.pages])}