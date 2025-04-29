# **Product Requirements Document (PRD): PDF Spell Checker Tool**  
**Version:** 1.0  
**Author:** Arun Kishore  
**Date:** 2025-03-02 

---

## **1. Overview**  
### **1.1 Purpose**  
A Python-based tool to identify spelling errors in PDFs by comparing extracted words against user-provided dictionaries. The tool will provide an interactive GUI (Streamlit), exportable results, and a highlighted PDF for corrections.  

### **1.2 Target Users**  
- Editors, proofreaders, and authors.  
- Legal/medical professionals verifying document accuracy.  
- Non-technical users needing a simple spell-check workflow.  

### **1.3 Key Features**  
- Upload PDFs and multiple `.txt` dictionaries.  
- Case-insensitive spell-check with configurable word cleaning.  
- Interactive misspelling list with occurrence counts and page numbers.  
- Export results (CSV) and highlighted PDFs.  

---

## **2. Requirements**  
### **2.1 Functional Requirements**  
| ID  | Requirement | Priority |  
|-----|------------|----------|  
| FR1 | Accept PDF and `.txt` dictionary uploads via GUI. | High |  
| FR2 | Extract words + locations from PDF using `pymupdf`. | High |  
| FR3 | Clean words (lowercase, strip punctuation, preserve hyphens). | High |  
| FR4 | Skip words containing digits. | Medium |  
| FR5 | Flag words not found in any dictionary. | High |  
| FR6 | Display misspellings with checkboxes, counts, and page numbers. | High |  
| FR7 | Export results to CSV (Word, Occurrences, Pages). | Medium |  
| FR8 | Generate PDF with yellow cloud highlights for selected words. | High |  

### **2.2 Non-Functional Requirements**  
| ID  | Requirement |  
|-----|------------|  
| NFR1 | Support Python ≥3.12.0. |  
| NFR2 | Use `streamlit` for GUI and `pymupdf` for PDF processing. |  
| NFR3 | Handle English-language text only. |  
| NFR4 | Ignore performance optimizations (v1 scope). |  

---

## **3. User Flow**  
1. **Upload Phase**:  
   - User uploads a PDF and ≥1 `.txt` dictionary files.  
2. **Processing Phase**:  
   - Tool extracts words, cleans them, and checks against dictionaries.  
3. **Review Phase**:  
   - User selects misspellings from an interactive table.  
4. **Export Phase**:  
   - User exports CSV or highlighted PDF.  

---

## **4. Technical Specifications**  
### **4.1 Data Processing**  
- **Word Extraction**:  
  - Use `pymupdf`’s `page.get_text("words")` to get words + bounding boxes.  
- **Cleaning Rules**:  
  - Convert to lowercase.  
  - Remove all non-alphanumeric characters except hyphens (`re.sub(r"[^a-z-]", "", word)`).  
  - Strip leading/trailing hyphens (`word.strip("-")`).  
- **Exclusions**:  
  - Discard words with digits (`any(c.isdigit() for c in word)`).  

### **4.2 Highlighting Method**  
- Use `page.add_rect_annot()` with `fill=(1, 1, 0)` (yellow) for cloud effect.  

### **4.3 Output Formats**  
| Output | Format | Example |  
|--------|--------|---------|  
| Misspelling Report | CSV | `"garantee", 3, "Page 1, Page 7"` |  
| Highlighted PDF | Annotated PDF | Original PDF with yellow rectangles over misspellings. |  

---

## **5. UI/UX Specifications**  
### **5.1 Streamlit GUI Layout**  
1. **Header**: Tool title and description.  
2. **File Uploaders**:  
   - PDF upload (required).  
   - Dictionary upload (≥1 `.txt` files, optional drag-and-drop).  
3. **Process Button**: Triggers spell-check.  
4. **Results Section**:  
   - Table with columns: `Word`, `Occurrences`, `Pages` (selectable rows).  
   - Buttons: "Export to CSV" and "Generate Highlighted PDF".  

### **5.2 Mockup**  
```plaintext
[PDF Spell Checker]  
Upload PDF: [Browse...]  
Upload Dictionaries: [Browse...] (multiple allowed)  
[Process]  

Results:  
☑ "garantee" (3 occurrences) - Pages: 1, 7  
☐ "recieve" (1 occurrence) - Page: 3  

[Export to CSV]  [Highlight PDF]  
```

---

## **6. Validation & Edge Cases**  
| Scenario | Handling |  
|----------|---------|  
| No dictionaries uploaded | Show error: "At least 1 dictionary required." |  
| Non-PDF upload | Reject with error: "Invalid file type." |  
| Empty/malformed dictionary | Skip empty lines; warn: "X empty lines ignored." |  
| Zero misspellings | Show: "No misspellings found." |  

---

## **7. Dependencies**  
- Python 3.12.0+  
- Libraries:  
  - `streamlit` (GUI)  
  - `pymupdf` (PDF processing)  

---

## **8. Success Metrics**  
- **Usability**: >90% of test users complete spell-check without documentation.  
- **Accuracy**: <1% false positives in word detection (manual QA).  

---

## **9. Open Issues**  
- Future support for multi-language dictionaries.  
- Batch processing for multiple PDFs (v2).  

---

**Approvals**  
| Role | Name | Date |  
|------|------|------|  
| PM | [Name] | [Date] |  
| Eng | [Name] | [Date] |  

--- 

**PRD Feedback**  
- [ ] Reviewed by Engineering  
- [ ] Reviewed by Design  
- [ ] Approved by Stakeholders