import streamlit as st
from deep_translator import GoogleTranslator

# Page config
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="centered"
)

# Blue theme CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
    }
    
    h1, h2, h3 {
        color: #1e40af;
    }
    
    .stButton > button {
        background-color: #2563eb;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .stTextArea textarea {
        border: 2px solid #dbeafe;
        border-radius: 10px;
    }
    
    hr {
        border: 1px solid #dbeafe;
        margin: 2rem 0;
    }
    
    /* Better quick buttons */
    .quick-btn {
        margin: 5px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Get languages with PROPER NAMES
def get_languages():
    """Get languages with actual names"""
    # Manual list with proper display names
    languages = {
        'Arabic': 'ar',
        'Bengali': 'bn',
        'Chinese (Simplified)': 'zh-cn',
        'Chinese (Traditional)': 'zh-tw',
        'Dutch': 'nl',
        'English': 'en',
        'French': 'fr',
        'German': 'de',
        'Greek': 'el',
        'Hebrew': 'he',
        'Hindi': 'hi',
        'Italian': 'it',
        'Japanese': 'ja',
        'Korean': 'ko',
        'Persian': 'fa',
        'Polish': 'pl',
        'Portuguese': 'pt',
        'Russian': 'ru',
        'Spanish': 'es',
        'Swedish': 'sv',
        'Thai': 'th',
        'Turkish': 'tr',
        'Ukrainian': 'uk',
        'Urdu': 'ur',
        'Vietnamese': 'vi'
    }
    return dict(sorted(languages.items()))

# Load languages
LANGUAGES = get_languages()

def translate_text(text, target_lang):
    """Simple translation function"""
    try:
        if not text or not text.strip():
            return "Please enter text to translate."
        
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
    
    if input_text:
        st.caption(f"📊 Characters: {len(input_text)}")

with col2:
    # Language selection
    st.subheader("Translate to:")
    
    # Language dropdown with PROPER NAMES
    target_language_name = st.selectbox(
        "Select language:",
        options=list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index('Spanish'),
        key="language"
    )
    
    target_language_code = LANGUAGES[target_language_name]
    
    # HORIZONTAL Quick translate buttons with FULL NAMES
    st.subheader("Quick Translate:")
    
    # Create 3 columns for buttons
    qcol1, qcol2, qcol3 = st.columns(3)
    
    with qcol1:
        if st.button("🇪🇸 Spanish", use_container_width=True, key="btn_es"):
            target_language_name = "Spanish"
            target_language_code = LANGUAGES["Spanish"]
    
    with qcol2:
        if st.button("🇫🇷 French", use_container_width=True, key="btn_fr"):
            target_language_name = "French"
            target_language_code = LANGUAGES["French"]
    
    with qcol3:
        if st.button("🇩🇪 German", use_container_width=True, key="btn_de"):
            target_language_name = "German"
            target_language_code = LANGUAGES["German"]
    
    # Add 3 more popular languages
    qcol4, qcol5, qcol6 = st.columns(3)
    
    with qcol4:
        if st.button("🇮🇹 Italian", use_container_width=True, key="btn_it"):
            target_language_name = "Italian"
            target_language_code = LANGUAGES["Italian"]
    
    with qcol5:
        if st.button("🇯🇵 Japanese", use_container_width=True, key="btn_ja"):
            target_language_name = "Japanese"
            target_language_code = LANGUAGES["Japanese"]
    
    with qcol6:
        if st.button("🇰🇷 Korean", use_container_width=True, key="btn_ko"):
            target_language_name = "Korean"
            target_language_code = LANGUAGES["Korean"]
    
    # Main translate button
    translate_btn = st.button("🚀 Translate", type="primary", use_container_width=True)

# Divider
st.markdown("---")

# Translation result
if translate_btn:
    if input_text.strip():
        with st.spinner("Translating..."):
            result = translate_text(input_text, target_language_code)
        
        # Display result
        st.subheader(f"Translation to {target_language_name}:")
        
        # Output text area
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
        
        # Simple stats in columns
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Input Length", f"{len(input_text)} chars")
        with col_stat2:
            st.metric("Output Length", f"{len(result)} chars")
            
    else:
        st.warning("⚠️ Please enter some text to translate.")

# Sidebar
with st.sidebar:
    st.header("ℹ️ How to Use")
    st.write("""
    1. **Type** your text in the box
    2. **Select** target language from dropdown
    **OR** click a quick language button
    3. **Click** Translate
    4. **Copy** the result if needed
    
    **Quick Languages Available:**
    - Spanish, French, German
    - Italian, Japanese, Korean
    """)
    
    st.info(f"✅ {len(LANGUAGES)} languages available")

# Footer
st.markdown("---")
st.caption("Built with Streamlit • Powered by Google Translate")
