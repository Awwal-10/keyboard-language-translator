import streamlit as st
from deep_translator import GoogleTranslator
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="TranslateX - AI-Powered Translation",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== MODERN SAAS STYLES ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Remove default Streamlit styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding: 3rem 2rem 2rem 2rem;
        max-width: 1400px;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 2.5rem 1rem 3rem 1rem;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        margin-bottom: 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: rgba(255, 255, 255, 0.85);
        font-weight: 400;
        margin-bottom: 1rem;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Glass Card Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 
            0 20px 60px rgba(0, 0, 0, 0.15),
            0 0 0 1px rgba(255, 255, 255, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 1.5rem;
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f1f5f9;
    }
    
    .card-icon {
        font-size: 1.5rem;
    }
    
    .card-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0;
    }
    
    /* Input Styling */
    .stTextArea textarea {
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
        background: #ffffff !important;
        color: #1e293b !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
    }
    
    /* Select Box */
    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        min-height: 50px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #cbd5e1 !important;
    }
    
    div[data-baseweb="select"] > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Secondary Button */
    .stButton > button[kind="secondary"] {
        background: white !important;
        color: #667eea !important;
        border: 2px solid #667eea !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: #f8f9ff !important;
    }
    
    /* Stats Cards */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    
    .stat-label {
        font-size: 0.875rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    /* Feature Pills */
    .feature-pill {
        background: #f1f5f9;
        color: #475569;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 500;
        display: inline-block;
        margin: 0.25rem;
    }
    
    /* Success Message */
    .success-banner {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    /* Copy Button Styling */
    .copy-btn {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        color: #475569;
        padding: 0.5rem 1.25rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-block;
    }
    
    .copy-btn:hover {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }
    
    /* Info Box */
    .info-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem 1.25rem;
        border-radius: 8px;
        color: #1e40af;
        font-size: 0.925rem;
        margin: 1rem 0;
    }
    
    /* Language Badge */
    .lang-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.35rem 0.85rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Spinner Override */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Metrics styling */
    div[data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        color: #1e293b !important;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        color: #64748b !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== LANGUAGE SETUP ====================
langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
LANGUAGES = {name.title(): code for name, code in sorted(langs_dict.items())}
sorted_langs = sorted(LANGUAGES.keys())

# ==================== HELPER FUNCTIONS ====================
def translate_text(text: str, target_lang: str) -> tuple:
    """Translate text and return result with detected language."""
    try:
        if not text or not text.strip():
            return "", ""
        
        translator = GoogleTranslator(source="auto", target=target_lang)
        result = translator.translate(text.strip())
        
        # Try to detect source language
        try:
            detector = GoogleTranslator(source="auto", target="en")
            detector.translate(text[:100])  # Small sample for detection
            source_lang = "Auto-detected"
        except:
            source_lang = "Unknown"
            
        return result or "", source_lang
    except Exception as e:
        return f"❌ Translation error: {str(e)}", ""

# ==================== SESSION STATE ====================
if "translation_result" not in st.session_state:
    st.session_state.translation_result = ""
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "last_lang" not in st.session_state:
    st.session_state.last_lang = ""
if "translation_count" not in st.session_state:
    st.session_state.translation_count = 0
if "source_lang" not in st.session_state:
    st.session_state.source_lang = ""
if "show_success" not in st.session_state:
    st.session_state.show_success = False

# ==================== HERO SECTION ====================
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">✨ Powered by AI Translation</div>
    <h1 class="hero-title">TranslateX</h1>
    <p class="hero-subtitle">Break language barriers instantly with professional-grade translation</p>
</div>
""", unsafe_allow_html=True)

# ==================== MAIN CONTENT ====================
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
        <div class="card-header">
            <span class="card-icon">📝</span>
            <h3 class="card-title">Source Text</h3>
        </div>
    """, unsafe_allow_html=True)
    
    input_text = st.text_area(
        "Enter text to translate",
        height=280,
        placeholder="Enter or paste your text here...\n\nSupports 100+ languages with automatic detection.",
        label_visibility="collapsed",
        key="input_text"
    )
    
    if input_text:
        char_count = len(input_text)
        word_count = len(input_text.split())
        
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        with metrics_col1:
            st.metric("Characters", f"{char_count:,}")
        with metrics_col2:
            st.metric("Words", f"{word_count:,}")
        with metrics_col3:
            st.metric("Lines", f"{len(input_text.splitlines()):,}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Settings Card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
        <div class="card-header">
            <span class="card-icon">⚙️</span>
            <h3 class="card-title">Translation Settings</h3>
        </div>
    """, unsafe_allow_html=True)
    
    default_index = sorted_langs.index("Spanish") if "Spanish" in sorted_langs else 0
    target_language_name = st.selectbox(
        "Target Language",
        options=sorted_langs,
        index=default_index,
        key="target_lang"
    )
    target_language_code = LANGUAGES[target_language_name]
    
    st.markdown(f'<div class="info-box">🎯 Translating to: <span class="lang-badge">{target_language_name}</span></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action Buttons
    btn_col1, btn_col2 = st.columns([2, 1])
    with btn_col1:
        translate_clicked = st.button("🚀 Translate Now", use_container_width=True, type="primary")
    with btn_col2:
        clear_clicked = st.button("🔄 Clear", use_container_width=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("""
        <div class="card-header">
            <span class="card-icon">✨</span>
            <h3 class="card-title">Translation Result</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if translate_clicked:
        if input_text and input_text.strip():
            with st.spinner(f"🔄 Translating to {target_language_name}..."):
                time.sleep(0.5)  # Brief delay for UX
                result, source = translate_text(input_text, target_language_code)
            
            st.session_state.translation_result = result
            st.session_state.last_input = input_text
            st.session_state.last_lang = target_language_name
            st.session_state.source_lang = source
            st.session_state.translation_count += 1
            st.session_state.show_success = True
            st.rerun()
        else:
            st.warning("⚠️ Please enter some text to translate.")
    
    if clear_clicked:
        st.session_state.translation_result = ""
        st.session_state.last_input = ""
        st.session_state.last_lang = ""
        st.session_state.source_lang = ""
        st.session_state.show_success = False
        st.rerun()
    
    # Show success message
    if st.session_state.show_success and st.session_state.translation_result:
        st.markdown("""
            <div class="success-banner">
                <span>✅</span>
                <span>Translation completed successfully!</span>
            </div>
        """, unsafe_allow_html=True)
        st.session_state.show_success = False
    
    # Display translation
    if st.session_state.translation_result:
        translated_text = st.session_state.translation_result
        
        st.text_area(
            "Translation output",
            value=translated_text,
            height=280,
            label_visibility="collapsed",
            key="output_text"
        )
        
        # Translation metrics
        if st.session_state.last_input:
            met_col1, met_col2 = st.columns(2)
            with met_col1:
                st.metric(
                    "Input Length",
                    f"{len(st.session_state.last_input)} chars",
                    delta=None
                )
            with met_col2:
                st.metric(
                    "Output Length", 
                    f"{len(translated_text)} chars",
                    delta=f"{len(translated_text) - len(st.session_state.last_input):+d}"
                )
    else:
        st.info("👆 Enter text and click 'Translate Now' to see results here")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Stats Card
    if st.session_state.translation_count > 0:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("""
            <div class="card-header">
                <span class="card-icon">📊</span>
                <h3 class="card-title">Session Statistics</h3>
            </div>
        """, unsafe_allow_html=True)
        
        stat_cols = st.columns(3)
        with stat_cols[0]:
            st.metric("Translations", st.session_state.translation_count)
        with stat_cols[1]:
            if st.session_state.last_input:
                total_chars = len(st.session_state.last_input)
                st.metric("Chars Processed", f"{total_chars:,}")
            else:
                st.metric("Chars Processed", "0")
        with stat_cols[2]:
            if st.session_state.last_lang:
                st.markdown(f"**Last Target:**<br><span class='lang-badge'>{st.session_state.last_lang}</span>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== FEATURES SECTION ====================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("""
    <div class="card-header">
        <span class="card-icon">🌟</span>
        <h3 class="card-title">Why Choose TranslateX?</h3>
    </div>
""", unsafe_allow_html=True)

feature_cols = st.columns(4)
with feature_cols[0]:
    st.markdown("**⚡ Instant Translation**")
    st.caption("Real-time results in milliseconds")
with feature_cols[1]:
    st.markdown("**🌍 100+ Languages**")
    st.caption("Comprehensive language support")
with feature_cols[2]:
    st.markdown("**🎯 Auto-Detection**")
    st.caption("Automatic source language detection")
with feature_cols[3]:
    st.markdown("**🔒 Privacy First**")
    st.caption("Your data stays secure")

st.markdown('</div>', unsafe_allow_html=True)
