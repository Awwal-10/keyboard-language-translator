import streamlit as st
from deep_translator import GoogleTranslator
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="TranslateX - Professional Translation",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== PROFESSIONAL SAAS STYLES ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Base styles */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif !important;
        color: #e2e8f0 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main background */
    .main {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        padding: 0;
    }
    
    .block-container {
        padding: 3rem 2rem;
        max-width: 1200px;
    }
    
    /* Force all text to be visible */
    p, span, div, label, input, textarea, select, h1, h2, h3, h4, h5, h6 {
        color: #e2e8f0 !important;
    }
    
    /* Header */
    .app-header {
        text-align: center;
        margin-bottom: 3rem;
        padding-bottom: 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .app-logo {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff !important;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
    }
    
    .app-tagline {
        font-size: 1rem;
        color: #94a3b8 !important;
        font-weight: 400;
    }
    
    /* Main translation card */
    .translation-card {
        background: #1e293b;
        border-radius: 16px;
        padding: 0;
        border: 1px solid #334155;
        overflow: hidden;
    }
    
    .card-section {
        padding: 2rem;
    }
    
    .section-divider {
        height: 1px;
        background: #334155;
        margin: 0;
    }
    
    .section-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94a3b8 !important;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Text areas - force white text */
    .stTextArea textarea {
        background: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-size: 0.95rem !important;
        padding: 1rem !important;
        line-height: 1.6 !important;
        transition: border-color 0.2s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        outline: none !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #64748b !important;
    }
    
    .stTextArea textarea:disabled {
        opacity: 0.5;
    }
    
    /* Select boxes - force white text */
    div[data-baseweb="select"] > div {
        background: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        min-height: 48px !important;
        transition: border-color 0.2s ease !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #475569 !important;
    }
    
    div[data-baseweb="select"] > div:focus-within {
        border-color: #3b82f6 !important;
    }
    
    div[data-baseweb="select"] div {
        color: #ffffff !important;
    }
    
    div[data-baseweb="select"] span {
        color: #ffffff !important;
    }
    
    div[data-baseweb="select"] input {
        color: #ffffff !important;
    }
    
    div[data-baseweb="select"] svg {
        fill: #94a3b8 !important;
    }
    
    /* Dropdown menu */
    ul[role="listbox"] {
        background: #1e293b !important;
        border: 1px solid #334155 !important;
    }
    
    ul[role="listbox"] li {
        color: #ffffff !important;
        background: #1e293b !important;
    }
    
    ul[role="listbox"] li:hover {
        background: #334155 !important;
    }
    
    ul[role="listbox"] li[aria-selected="true"] {
        background: #3b82f6 !important;
        color: #ffffff !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        letter-spacing: 0.01em !important;
    }
    
    .stButton > button:hover {
        background: #2563eb !important;
        transform: translateY(-1px) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    .stButton > button p {
        color: #ffffff !important;
    }
    
    /* Info text */
    .info-text {
        color: #94a3b8 !important;
        font-size: 0.875rem;
        margin-top: 0.75rem;
    }
    
    .info-highlight {
        color: #3b82f6 !important;
        font-weight: 500;
    }
    
    /* Metrics - force white text */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #ffffff !important;
    }
    
    div[data-testid="stMetricValue"] div {
        color: #ffffff !important;
    }
    
    div[data-testid="stMetricValue"] label {
        color: #ffffff !important;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        color: #94a3b8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    div[data-testid="stMetricLabel"] div {
        color: #94a3b8 !important;
    }
    
    div[data-testid="stMetricLabel"] label {
        color: #94a3b8 !important;
    }
    
    /* Remove metric delta */
    div[data-testid="stMetricDelta"] {
        display: none !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #3b82f6 !important;
    }
    
    /* Warning/Info boxes */
    .stAlert {
        background: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    
    .stAlert div {
        color: #e2e8f0 !important;
    }
    
    .stAlert p {
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== LANGUAGE SETUP ====================
langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
LANGUAGES = {name.title(): code for name, code in sorted(langs_dict.items())}
sorted_langs = sorted(LANGUAGES.keys())

# ==================== HELPER FUNCTIONS ====================
def translate_text(text: str, target_lang: str) -> str:
    """Translate text to target language."""
    try:
        if not text or not text.strip():
            return ""
        translator = GoogleTranslator(source="auto", target=target_lang)
        result = translator.translate(text.strip())
        return result or ""
    except Exception as e:
        return f"Translation error: {str(e)}"

# ==================== SESSION STATE ====================
if "translation_result" not in st.session_state:
    st.session_state.translation_result = ""
if "translation_count" not in st.session_state:
    st.session_state.translation_count = 0

# ==================== HEADER ====================
st.markdown("""
<div class="app-header">
    <div class="app-logo">TranslateX</div>
    <div class="app-tagline">Professional translation platform</div>
</div>
""", unsafe_allow_html=True)

# ==================== MAIN LAYOUT ====================
st.markdown('<div class="translation-card">', unsafe_allow_html=True)

# Input Section
st.markdown('<div class="card-section">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Input</div>', unsafe_allow_html=True)

input_text = st.text_area(
    "Input text",
    height=200,
    placeholder="Enter text to translate...",
    label_visibility="collapsed",
    key="input_text"
)

if input_text:
    char_count = len(input_text)
    word_count = len(input_text.split())
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Characters", f"{char_count:,}")
    with col2:
        st.metric("Words", f"{word_count:,}")

st.markdown('</div>', unsafe_allow_html=True)

# Divider
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Settings Section
st.markdown('<div class="card-section">', unsafe_allow_html=True)

col_select, col_button = st.columns([3, 1])

with col_select:
    st.markdown('<div class="section-label">Target Language</div>', unsafe_allow_html=True)
    default_index = sorted_langs.index("Spanish") if "Spanish" in sorted_langs else 0
    target_language_name = st.selectbox(
        "Target language",
        options=sorted_langs,
        index=default_index,
        label_visibility="collapsed",
        key="target_lang"
    )

with col_button:
    st.markdown('<div class="section-label" style="opacity: 0;">Action</div>', unsafe_allow_html=True)
    translate_clicked = st.button("Translate", use_container_width=True, type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Divider
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Output Section
st.markdown('<div class="card-section">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Translation</div>', unsafe_allow_html=True)

# Handle translation
if translate_clicked:
    if input_text and input_text.strip():
        target_code = LANGUAGES[target_language_name]
        with st.spinner("Translating..."):
            time.sleep(0.3)
            result = translate_text(input_text, target_code)
        st.session_state.translation_result = result
        st.session_state.translation_count += 1
        st.rerun()
    else:
        st.warning("Please enter text to translate")

# Display result
if st.session_state.translation_result:
    st.text_area(
        "Translation result",
        value=st.session_state.translation_result,
        height=200,
        label_visibility="collapsed",
        key="output_text"
    )
    
    result_chars = len(st.session_state.translation_result)
    st.markdown(f'<div class="info-text">Output: <span class="info-highlight">{result_chars:,} characters</span> • Translated to <span class="info-highlight">{target_language_name}</span></div>', unsafe_allow_html=True)
else:
    st.text_area(
        "Translation result",
        value="",
        height=200,
        placeholder="Translation will appear here...",
        label_visibility="collapsed",
        key="output_text_empty",
        disabled=True
    )

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Session stats (only show if translations have been made)
if st.session_state.translation_count > 0:
    st.markdown(f'<div class="info-text" style="text-align: center; margin-top: 1.5rem;">Session: <span class="info-highlight">{st.session_state.translation_count}</span> translation{"s" if st.session_state.translation_count != 1 else ""} completed</div>', unsafe_allow_html=True)
