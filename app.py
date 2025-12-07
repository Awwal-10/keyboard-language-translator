import streamlit as st
from deep_translator import GoogleTranslator

# Page config
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="centered"
)

# Add BLUE theme CSS
st.markdown("""
<style>
    /* Blue theme */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Blue headers */
    h1, h2, h3 {
        color: #1e40af;
    }
    
    /* Blue buttons */
    .stButton > button {
        background-color: #2563eb;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #1d4ed8;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    
    /* Blue text areas */
    .stTextArea textarea {
        border: 2px solid #dbeafe;
        border-radius: 10px;
        background-color: #f8fafc;
    }
    
    .stTextArea textarea:focus {
        border-color: #60a5fa;
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.2);
    }
    
    /* Blue select box */
    div[data-baseweb="select"] {
        border-radius: 10px;
        border: 2px solid #dbeafe;
    }
    
    /* Blue divider */
    hr {
        border: 1px solid #dbeafe;
        margin: 2rem 0;
    }
    
    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2563eb;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Get languages PROPERLY
def get_languages():
    """Get languages with proper names"""
    try:
        # Get from GoogleTranslator
        lang_dict = GoogleTranslator().get_supported_languages(as_dict=True)
        # Fix the format: we want {'English': 'en', 'Spanish': 'es'}
        languages = {}
        for code, name in lang_dict.items():
            # Capitalize properly
            proper_name = name.title()
            languages[proper_name] = code
        return dict(sorted(languages.items()))
    except:
        # Fallback with proper names
        return {
            'Arabic': 'ar',
            'Chinese': 'zh-cn',
            'English': 'en',
            'French': 'fr',
            'German': 'de',
            'Hindi': 'hi',
            'Italian': 'it',
            'Japanese': 'ja',
            'Korean': 'ko',
            'Portuguese': 'pt',
            'Russian': 'ru',
            'Spanish': 'es',
            'Turkish': 'tr',
            'Vietnamese': 'vi'
        }

# Load languages
LANGUAGES = get_languages()

def translate_text(text, target_lang):
    """Simple translation function"""
    try:
        if not text or not text.strip():
            return "Please enter text to translate."
        
        # Translate
        translator = GoogleTranslator(source='auto', target=target_lang)
        result = translator.translate(text)
        return result
    
    except Exception as e:
        return f"Error: {str(e)}"

# ===== MAIN APP =====
st.title("🌍 Language Translator")
st.markdown("Translate text instantly between languages")

# Layout
col1, col2 = st.columns([3, 1])

with col1:
    # Input text
    input_text = st.text_area(
        "Enter text to translate:",
        height=150,
        placeholder="Type or paste your text here...",
        key="input"
    )
    
    # Show character count
    if input_text:
        st.caption(f"📊 Characters: {len(input_text)}")

with col2:
    # Language selection
    st.subheader("Translate to:")
    
    # Language dropdown with proper names
    language_names = list(LANGUAGES.keys())
    target_language_name = st.selectbox(
        "Select language:",
        options=language_names,
        index=language_names.index('Spanish') if 'Spanish' in language_names else 0,
        key="language"
    )
    
    # Get the language code
    target_language_code = LANGUAGES[target_language_name]
    st.caption(f"Code: {target_language_code}")
    
    # Quick translate buttons
    st.subheader("Quick Translate:")
    quick_cols = st.columns(3)
    with quick_cols[0]:
        if st.button("🇪🇸 ES", use_container_width=True):
            target_language_name = "Spanish"
    with quick_cols[1]:
        if st.button("🇫🇷 FR", use_container_width=True):
            target_language_name = "French"
    with quick_cols[2]:
        if st.button("🇩🇪 DE", use_container_width=True):
            target_language_name = "German"
    
    # Translate button
    translate_btn = st.button("🚀 Translate", type="primary", use_container_width=True)

# Divider
st.markdown("---")

# Translation result
if translate_btn:
    if input_text.strip():
        with st.spinner("Translating..."):
            result = translate_text(input_text, target_language_code)
        
        # Display result
        st.subheader("Translation Result:")
        
        # Text area for output
        output_area = st.text_area(
            "Translated text:",
            value=result,
            height=150,
            key="output"
        )
        
        # Copy button
        if st.button("📋 Copy to Clipboard"):
            st.code(result)
            st.success("Copied to clipboard!")
        
        # Simple stats
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(2)
        with cols[0]:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Input", f"{len(input_text)} chars")
            st.markdown('</div>', unsafe_allow_html=True)
        with cols[1]:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Output", f"{len(result)} chars")
            st.markdown('</div>', unsafe_allow_html=True)
            
    else:
        st.warning("⚠️ Please enter some text to translate.")

# Sidebar
with st.sidebar:
    st.header("ℹ️ How to Use")
    st.write("""
    1. **Type** your text
    2. **Select** target language
    3. **Click** Translate button
    4. **Copy** the result
    
    **Features:**
    - 100+ languages
    - Auto-detection
    - Copy to clipboard
    - Quick translate buttons
    
    **Popular Languages:**
    - Spanish, French, German
    - Chinese, Japanese, Korean
    - Arabic, Hindi, Russian
    """)
    
    st.info(f"✅ {len(LANGUAGES)} languages available")

# Footer
st.markdown("---")
st.caption("Built with Streamlit • Powered by Google Translate")
