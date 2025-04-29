# **To-Do List: PDF Spell Checker Tool**  
**Based on PRD v1.0**  

---

## **1. Setup & Configuration**  
- [x] Create Python 3.12 virtual environment.  
- [x] Install dependencies: `streamlit`, `pymupdf`.  
- [x] Initialize Git repository with `.gitignore` for Python/IDE files.  

---

## **2. Backend Implementation**  
### **Core Logic**  
- [x] **PDF Processing**  
  - [x] Write function to extract words + bounding boxes/pages using `pymupdf`.  
  - [x] Handle hyphenated words as single tokens (e.g., "state-of-the-art").  
- [x] **Word Cleaning**  
  - [x] Implement regex to strip non-alphanumeric/hyphen characters.  
  - [x] Convert words to lowercase.  
  - [x] Filter out words with digits (e.g., "B2B").  
- [x] **Dictionary Handling**  
  - [x] Load `.txt` files into a lowercase set, ignoring empty lines.  
  - [x] Validate dictionary format (UTF-8, one word per line).  
- [x] **Spell Check**  
  - [x] Compare cleaned words against dictionary set.  
  - [x] Track misspelled words with page numbers and counts.  
- [x] **Highlighting**  
  - [x] Implement `highlight_pdf()` to add yellow cloud annotations using `pymupdf`.  

### **Output Generation**  
- [x] **CSV Export**  
  - [x] Generate CSV with columns: `Word, Occurrences, Pages`.  
- [x] **PDF Export**  
  - [x] Save a copy of the PDF with annotations for selected words.  

---

## **3. Frontend (Streamlit GUI)**  
- [x] **File Uploaders**  
  - [x] Add PDF upload widget (required, accept `.pdf` only).  
  - [x] Add dictionary upload widget (accept `.txt`, multiple files allowed).  
- [x] **Process Button**  
  - [x] Trigger backend processing on click.  
  - [x] Show loading spinner during execution.  
- [x] **Results Display**  
  - [x] Render table of misspelled words with checkboxes.  
  - [x] Show occurrence counts and page numbers for selected words.  
- [x] **Export Buttons**  
  - [x] Add "Export to CSV" button (enabled only if words are selected).  
  - [x] Add "Generate Highlighted PDF" button (enabled only if words are selected).  

---

## **4. Error Handling & Validation**  
- [x] **Input Validation**  
  - [x] Show error if no PDF/dictionary is uploaded.  
  - [x] Reject non-PDF/non-TXT files with alerts.  
- [x] **Edge Cases**  
  - [x] Handle empty/malformed dictionaries (skip invalid lines).  
  - [x] Show "No misspellings found" message if results are empty.  

---

## **5. Testing**  
### **Unit Tests**  
- [ ] Test word cleaning (e.g., "Hello!" → "hello", "don’t" → "dont").  
- [ ] Test hyphen handling ("state-of-the-art" → single word).  
- [ ] Test digit exclusion ("123test" → skipped).  
### **Integration Tests**  
- [ ] End-to-end test with sample PDF/dictionary.  
- [ ] Validate CSV/PDF exports match selected words.  
### **User Testing**  
- [ ] Conduct usability tests with non-technical users.  

---

## **6. Documentation**  
- [ ] **User Guide**  
  - [ ] Write README with setup/usage instructions.  
  - [ ] Add screenshots of the GUI.  
- [ ] **Code Documentation**  
  - [ ] Add docstrings for core functions.  
  - [ ] Comment complex logic (e.g., regex, bounding box math).  

---

## **7. Deployment Prep**  
- [ ] Create `requirements.txt` with pinned dependencies.  
- [ ] Test installation on fresh environment.  
- [ ] Draft release notes for v1.0.  

---