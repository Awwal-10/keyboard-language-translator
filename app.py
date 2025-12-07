import streamlit as st
from deep_translator import GoogleTranslator

# Page config
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="centered"
)

# Clean CSS
st.markdown("""
<style>
    .main {
        padding: 0 1rem;
    }
    
    h1 {
        color: #1e40af;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        background-color: #2563eb;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #1d4ed8;
    }
    
    .stTextArea textarea {
        border: 2px solid #dbeafe;
        border-radius: 10px;
        font-size: 16px;
    }
    
    .stSelectbox {
        margin-bottom: 1rem;
    }
    
    hr {
        border: 1px solid #dbeafe;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Languages
LANGUAGES = {
    'Arabic': 'ar',
    'Bengali': 'bn',
    'Chinese (Simplified)': 'zh-cn',
    'Chinese (Traditional)': 'zh-tw',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'English': 'en',
    'Finnish': 'fi',
    'French': 'fr',
    'German': 'de',
    'Greek': 'el',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Hungarian': 'hu',
    'Indonesian': 'id',
    'Italian': 'it',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Norwegian': 'no',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Spanish': 'es',
    'Swedish': 'sv',
    'Thai': 'th',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Vietnamese': 'vi'
}

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
        "**Enter text to translate:**",
        height=180,
        placeholder="Type or paste your text here...",
        key="input"
    )
    
    if input_text:
        st.caption(f"📊 **Characters:** {len(input_text)}")

with col2:
    st.subheader("🎯 Translation Settings")
    
    # Language dropdown only
    target_language_name = st.selectbox(
        "**Select target language:**",
        options=list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index('Spanish'),
        key="language_select"
    )
    
    target_language_code = LANGUAGES[target_language_name]
    st.caption(f"Language code: `{target_language_code}`")
    
    # Main translate button
    st.markdown("<br>", unsafe_allow_html=True)
    translate_btn = st.button("🚀 **TRANSLATE NOW**", type="primary", use_container_width=True)

# Divider
st.markdown("---")

# Translation result
if translate_btn:
    if input_text.strip():
        with st.spinner(f"Translating to {target_language_name}..."):
            result = translate_text(input_text, target_language_code)
        
        # Display result
        st.subheader(f"📤 Translation to {target_language_name}")
        
        # Output text area
        st.text_area(
            "**Translated text:**",
            value=result,
            height=180,
            key="output"
        )
        
        # Copy button
        if st.button("📋 Copy to Clipboard"):
            st.code(result, language='text')
            st.success("Copied to clipboard!")
        
        # Simple stats
        st.caption(f"📊 **Input:** {len(input_text)} characters | **Output:** {len(result)} characters")
            
    else:
        st.warning("⚠️ Please enter some text to translate.")

# Sidebar
with st.sidebar:
    st.header("ℹ️ How to Use")
    st.markdown("""
    1. **Type** your text in the box
    2. **Select** target language from dropdown
    3. **Click** TRANSLATE NOW button
    4. **Copy** the result if needed
    
    ### Features:
    - 30+ languages
    - Real-time translation
    - Auto language detection
    - Simple interface
    - Copy to clipboard
    """)
    
    st.info(f"**Languages available:** {len(LANGUAGES)}")

# Footer
st.markdown("---")
st.caption("🌐 *Built with Streamlit • Powered by Google Translate*")
