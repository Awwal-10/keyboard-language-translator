import streamlit as st
from deep_translator import GoogleTranslator

# Page config
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="wide"  # Changed to wide for better spacing
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
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 500;
        margin: 2px;
        white-space: nowrap;
    }
    
    .stButton > button:hover {
        background-color: #1d4ed8;
    }
    
    /* Make quick buttons wrap properly */
    .quick-buttons-container {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        margin: 10px 0;
    }
    
    /* Force quick buttons to show full text */
    .quick-button {
        min-width: 100px;
        flex: 1;
    }
    
    .stTextArea textarea {
        border: 2px solid #dbeafe;
        border-radius: 10px;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# Languages with FULL NAMES (truncated versions removed)
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

# Main layout with more space
col1, col2 = st.columns([7, 3])

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
    st.subheader("🎯 Target Language")
    
    # Language dropdown
    target_language_name = st.selectbox(
        "Select from all languages:",
        options=list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index('Spanish'),
        key="language_select"
    )
    
    target_language_code = LANGUAGES[target_language_name]
    st.caption(f"Language code: `{target_language_code}`")
    
    # --- QUICK TRANSLATE BUTTONS ---
    st.subheader("⚡ Quick Select")
    st.write("Click any button below:")
    
    # Create TWO ROWS of quick buttons
    # First row
    qrow1 = st.columns(4)
    with qrow1[0]:
        if st.button("🇪🇸 Spanish", use_container_width=True, key="btn_es"):
            target_language_name = "Spanish"
    with qrow1[1]:
        if st.button("🇫🇷 French", use_container_width=True, key="btn_fr"):
            target_language_name = "French"
    with qrow1[2]:
        if st.button("🇩🇪 German", use_container_width=True, key="btn_de"):
            target_language_name = "German"
    with qrow1[3]:
        if st.button("🇮🇹 Italian", use_container_width=True, key="btn_it"):
            target_language_name = "Italian"
    
    # Second row
    qrow2 = st.columns(4)
    with qrow2[0]:
        if st.button("🇯🇵 Japanese", use_container_width=True, key="btn_ja"):
            target_language_name = "Japanese"
    with qrow2[1]:
        if st.button("🇰🇷 Korean", use_container_width=True, key="btn_ko"):
            target_language_name = "Korean"
    with qrow2[2]:
        if st.button("🇷🇺 Russian", use_container_width=True, key="btn_ru"):
            target_language_name = "Russian"
    with qrow2[3]:
        if st.button("🇵🇹 Portuguese", use_container_width=True, key="btn_pt"):
            target_language_name = "Portuguese"
    
    # Third row
    qrow3 = st.columns(4)
    with qrow3[0]:
        if st.button("🇳🇱 Dutch", use_container_width=True, key="btn_nl"):
            target_language_name = "Dutch"
    with qrow3[1]:
        if st.button("🇹🇷 Turkish", use_container_width=True, key="btn_tr"):
            target_language_name = "Turkish"
    with qrow3[2]:
        if st.button("🇸🇪 Swedish", use_container_width=True, key="btn_sv"):
            target_language_name = "Swedish"
    with qrow3[3]:
        if st.button("🇵🇱 Polish", use_container_width=True, key="btn_pl"):
            target_language_name = "Polish"
    
    # Main translate button
    st.markdown("<br>", unsafe_allow_html=True)
    translate_btn = st.button("🚀 **TRANSLATE NOW**", type="primary", use_container_width=True)

# Divider
st.markdown("---")

# Translation result
if translate_btn:
    if input_text.strip():
        # Update code based on selected language
        target_language_code = LANGUAGES[target_language_name]
        
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
        
        # Action buttons
        col_copy, col_stats = st.columns([1, 3])
        with col_copy:
            if st.button("📋 Copy Translation"):
                st.code(result, language='text')
                st.success("Copied!")
        
        # Simple inline stats
        st.caption(f"📊 **Stats:** Input: {len(input_text)} chars → Output: {len(result)} chars")
            
    else:
        st.warning("⚠️ Please enter some text to translate.")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About This Tool")
    st.markdown("""
    ### How to Use:
    1. **Type** your text
    2. **Pick** a language:
       - Use dropdown for all languages
       - OR click quick buttons
    3. **Click** TRANSLATE NOW
    4. **Copy** if needed
    
    ### Quick Languages:
    🇪🇸 🇫🇷 🇩🇪 🇮🇹  
    🇯🇵 🇰🇷 🇷🇺 🇵🇹  
    🇳🇱 🇹🇷 🇸🇪 🇵🇱
    
    ### Features:
    - Real-time translation
    - 30+ languages
    - Auto language detection
    - Clean interface
    """)
    
    st.info(f"**Languages available:** {len(LANGUAGES)}")

# Footer
st.markdown("---")
st.caption("🌐 *Built with Streamlit • Powered by Google Translate*")
