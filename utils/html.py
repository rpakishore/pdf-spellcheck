CSS_STYLE: str = """<style>
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
</style>"""

FOOTER: str = """<div class="footer">
        Created and maintained by <a href='mailto:remaa@ae.ca'>Arun Kishore</a> | 
        Structural EIT, Vancouver Office
    </div>"""
