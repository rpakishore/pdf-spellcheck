# PDF Spell Checker

## Overview
A Streamlit-based web application designed to identify potential spelling errors within PDF documents by comparing extracted words against customizable engineering dictionary files. The tool provides an interactive interface for reviewing misspellings, selective export capabilities, and PDF highlighting functionality. Built specifically for engineering professionals to ensure technical document accuracy.

**Project Type:** Internal Tool  
**Status:** Active Development  

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Quality Management](#quality-management)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Installation

### Prerequisites
- Python >= 3.13
- Windows operating system (for batch file launcher)
- Web browser for Streamlit interface

### Quick Start
```bash
# Clone the repository
git clone https://gitlab.ae.ca/remaa/ae-pdf-spellcheck.git
cd ae-pdf-spellcheck

# Option 1: Use the Windows launcher (Recommended)
# Double-click Launch_SpellCheck.bat

# Option 2: Manual installation with uv
uv run --with streamlit==1.43.2 --with pymupdf==1.25.4 streamlit run SpellCheck.py
```

### Environment Setup
The application uses `uv` for dependency management. The launcher script will automatically install `uv` if not present and handle all dependency installation.

## Usage

### Basic Usage
1. **Launch Application:**
   - Double-click `Launch_SpellCheck.bat` (Windows)
   - Or run manually: `uv run streamlit run SpellCheck.py`

2. **Access Web Interface:**
   - Application opens automatically at `http://localhost:81`
   - Use the modern, professional web interface

### Common Use Cases

#### For Engineering Document Review
1. **Upload PDF:** Select your engineering document (reports, specifications, drawings)
2. **Select Dictionaries:** Choose from specialized engineering dictionaries:
   - `Mechanical.txt` - Mechanical engineering terms
   - `Structural.txt` - Structural engineering terminology  
   - `Civil.txt` - Civil engineering vocabulary
   - `Electrical.txt` - Electrical engineering terms
   - `Process.txt` - Process engineering terminology
   - `General.txt` - General engineering terms
   - `Eng_Dictionary.txt` - Comprehensive engineering dictionary

3. **Review Results:** Interactive table shows potential misspellings with:
   - Original word as found in document
   - Number of occurrences
   - Page numbers where word appears
   - Checkbox for selective inclusion

4. **Export Options:**
   - **CSV Export:** Download `misspelled_words.csv` with selected words
   - **Highlighted PDF:** Generate `highlighted.pdf` with yellow highlights on selected misspellings

## Configuration

### Dictionary Management
| Dictionary File | Purpose | Discipline |
|----------------|---------|------------|
| `General.txt` | Common engineering terms | All |
| `Mechanical.txt` | Mechanical systems | Mechanical |
| `Structural.txt` | Structural elements | Structural |
| `Civil.txt` | Civil engineering | Civil |
| `Electrical.txt` | Electrical systems| Electrical |
| `Process.txt` | Process engineering | Process |
| `Bridges.txt` | Bridge engineering  | Structural |
| `Instrumentation.txt` | Control systems  | Instrumentation |
| `Landscape.txt` | Landscape architecture | Landscape |
| `Eng_Dictionary.txt` | Comprehensive dictionary | All |

### Word Processing Rules
- **Case Insensitive:** All comparisons performed in uppercase
- **Character Cleaning:** Removes non-alphanumeric characters except hyphens
- **Hyphen Handling:** Preserves internal hyphens, strips leading/trailing
- **Digit Exclusion:** Words containing numbers are ignored
- **Empty Word Filtering:** Blank or whitespace-only words excluded

## Quality Management

### Quality Control Framework
This project implements formal quality controls for engineering document validation with external verification processes.

### Quality Control Roles
| Role | Responsibility | Contact | Sign-off Required |
|------|---------------|---------|-------------------|
| Subject Matter Expert | Engineering terminology validation | Engineering Team Leads | Yes |
| Engineer of Record | Technical oversight and approval | Arun Kishore - remaa@ae.ca | Yes |
| Document Quality Reviewer | Spell-check accuracy validation | Project Managers | Yes |

### Quality Control Procedures

#### Pre-Deployment Quality Gates
1. **Code Review** - Internal development team review
2. **Dictionary Validation** - Engineering terminology accuracy check
3. **False Positive Testing** - Validation against known correct technical documents
4. **User Acceptance Testing** - Testing by target engineering professionals
5. **Performance Validation** - Processing speed and accuracy benchmarks

#### Quality Control Deliverables
- [ ] **Dictionary Accuracy Report** - Validation of technical terminology
- [ ] **False Positive Analysis** - Rate of incorrect flagging
- [ ] **Performance Benchmarks** - Processing speed metrics
- [ ] **User Testing Results** - Feedback from engineering professionals
- [ ] **Technical Documentation** - Code quality and standards compliance

### Quality Standards and Metrics
- **Dictionary Accuracy:** >99% of flagged words are legitimate misspellings
- **Processing Speed:** <30 seconds for typical 50-page engineering document
- **False Positive Rate:** <5% for technical documents
- **User Satisfaction:** >90% of users find tool helpful for document review

## Development

### Local Development Setup
```bash
# Clone repository
git clone https://gitlab.ae.ca/remaa/ae-pdf-spellcheck.git
cd ae-pdf-spellcheck

# Install dependencies
uv sync

# Run in development mode
uv run streamlit run SpellCheck.py --browser.gatherUsageStats=False
```

### Project Structure
```
├── SpellCheck.py          # Main Streamlit application
├── CreateDict.py          # Dictionary creation utility
├── Launch_SpellCheck.bat  # Windows launcher script
├── Launch_CreateDict.bat  # Dictionary creator launcher
├── default_dict/          # Engineering dictionary files
│   ├── General.txt        # General engineering terms
│   ├── Mechanical.txt     # Mechanical engineering terms
│   ├── Structural.txt     # Structural engineering terms
│   ├── Civil.txt          # Civil engineering terms
│   ├── Electrical.txt     # Electrical engineering terms
│   ├── Process.txt        # Process engineering terms
│   ├── Bridges.txt        # Bridge engineering terms
│   ├── Instrumentation.txt# Instrumentation terms
│   ├── Landscape.txt      # Landscape architecture terms
│   └── Eng_Dictionary.txt # Comprehensive engineering dictionary
├── uv.lock               # Dependency lock file
├── PRD.md                # Product Requirements Document
├── README.md             # User-facing documentation
└── LICENSE               # MIT License
```

### Technical Architecture
- **Frontend:** Streamlit web interface with custom CSS styling
- **PDF Processing:** PyMuPDF (fitz) for text extraction and annotation
- **Word Processing:** Regex-based cleaning and normalization
- **Data Handling:** Pandas for result management and export
- **Caching:** Streamlit caching for dictionary loading performance

## Testing

### Manual Testing Process
```bash
# Test with sample engineering documents
1. Load application: Launch_SpellCheck.bat
2. Upload test PDF (engineering report/specification)
3. Select appropriate dictionaries
4. Verify misspelling detection accuracy
5. Test CSV export functionality
6. Test PDF highlighting feature
```

### Dictionary Validation
- Compare flagged words against known engineering terminology
- Validate technical abbreviations and acronyms
- Test hyphenated compound words
- Verify proper noun handling

### Performance Testing
- Test with large PDFs (100+ pages)
- Measure processing time and memory usage
- Validate highlight accuracy on complex layouts

## Deployment

### Production Environment
- **Hosting:** Local deployment via Windows batch files
- **Port:** 81 (configurable in launch script)
- **Theme:** Light theme with AE branding colors
- **Browser:** Auto-launch disabled for professional use

### Installation Package
The application is distributed as a complete package including:
- All Python source files
- Engineering dictionary files
- Windows launcher scripts
- Documentation (PDF and markdown)

## Troubleshooting

### Common Issues

**Issue:** "uv is not installed" error  
**Solution:** Allow the launcher script to automatically install uv, or manually install from https://astral.sh/uv/

**Issue:** Port 81 already in use  
**Solution:** Modify port number in `Launch_SpellCheck.bat` file

**Issue:** PDF won't upload  
**Solution:** Ensure PDF is not password-protected and file size is reasonable (<100MB)

**Issue:** No misspellings found in technical document  
**Solution:** Select appropriate engineering dictionaries for your discipline

**Issue:** Many false positives  
**Solution:** Use more comprehensive dictionaries or add custom terms to existing dictionary files

### Logs and Monitoring
- Streamlit logs available in terminal/command prompt
- Processing status shown in web interface
- Error messages displayed in browser console

### Performance Considerations
- Large PDFs (>50MB) may require additional processing time
- Multiple large dictionaries increase memory usage
- Complex PDF layouts may affect highlighting accuracy

## Contributing

### For Internal Contributors
- Follow existing code style and structure
- Test with various engineering document types
- Update dictionaries with new technical terminology
- Document any changes to word processing rules

### Adding New Dictionary Terms
1. Open appropriate dictionary file in `default_dict/`
2. Add new terms (one per line, any case)
3. Test with documents containing those terms
4. Update documentation if needed

### Code Review Requirements
- All changes reviewed by Engineer of Record
- Testing with representative engineering documents
- Performance impact assessment for large files

## License
MIT License - This software is open source and available for modification and distribution under MIT terms. See LICENSE file for full details.

## Support

### Team Contacts
- **Project Owner & Engineer of Record:** Arun Kishore - remaa@ae.ca
- **Organization:** Associated Engineering (B.C.) Ltd.
- **Office:** #500 - 2889 East 12th Avenue, Vancouver, BC V5M 4T5
- **Direct Phone:** 236.317.2201

### Client Information
- **Primary Users:** Engineering professionals (Structural, Mechanical, Civil, Electrical)
- **Use Case:** Technical document spell-checking and quality assurance
- **Industry:** Engineering consulting and design services

### Additional Resources
- **Product Requirements:** See PRD.md for detailed specifications
- **Technical Documentation:** See existing README.md for user instructions
- **Dictionary Management:** Use CreateDict.py for custom dictionary creation

---

## Additional Sections

### Security Considerations
- No sensitive data retention (PDFs processed locally)
- No network communication beyond initial dictionary loading
- Local file system access only for uploaded documents
- No user authentication required for internal tool use

### Data Handling
- **Input:** PDF documents and text dictionary files
- **Processing:** Temporary file handling with automatic cleanup
- **Output:** CSV files and annotated PDF documents
- **Privacy:** All processing occurs locally, no data transmission

### Dictionary Customization
Engineering professionals can customize dictionaries by:
- Adding discipline-specific terminology to existing files
- Creating new dictionary files in `default_dict/` folder
- Using `CreateDict.py` utility for batch dictionary creation
- Combining multiple dictionaries for comprehensive coverage

### Integration Points
- **PDF Readers:** Compatible with any PDF-generating software
- **Document Workflows:** Integrates into document review processes
- **Export Formats:** CSV output compatible with Excel and other analysis tools
- **Highlighting:** PDF annotations compatible with standard PDF viewers

---

*Last updated: May 2025 by Arun Kishore*
*Version: 1.0 - Production Ready*