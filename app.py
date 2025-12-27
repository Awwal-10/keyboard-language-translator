import streamlit as st
from deep_translator import GoogleTranslator

# Page config
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="centered"
)

# CSS Styling
st.markdown("""
<style>
    .main {
        padding: 2rem 1rem;
    }
    
    h1 {
        color: #1e40af;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%);
        transform: translateY(-2px);
    }
    
    .stTextArea textarea {
        border: 2px solid #dbeafe;
        border-radius: 12px;
        font-size: 16px;
        padding: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #dbeafe, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Languages dictionary
LANGUAGES = {
    'Afrikaans': 'af',
    'Albanian': 'sq',
    'Arabic': 'ar',
    'Armenian': 'hy',
    'Bengali': 'bn',
    'Bulgarian': 'bg',
    'Catalan': 'ca',
    'Chinese (Simplified)': 'zh-cn',
    'Chinese (Traditional)': 'zh-tw',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'English': 'en',
    'Estonian': 'et',
    'Filipino': 'tl',
    'Finnish': 'fi',
    'French': 'fr',
    'German': 'de',
    'Greek': 'el',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Hungarian': 'hu',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Malay': 'ms',
    'Norwegian': 'no',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Serbian': 'sr',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Spanish': 'es',
    'Swedish': 'sv',
    'Tamil': 'ta',
    'Thai': 'th',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Vietnamese': 'vi',
    'Welsh': 'cy'
}

def translate_text(text, target_lang):
    """Translate text to target language"""
    try:
        if not text or not text.strip():
            return None
        
        translator = GoogleTranslator(source='auto', target=target_lang)
        result = translator.translate(text.strip())
        return result if result else None
    
    except Exception as e:
        return f"❌ Translation error: {str(e)}"

# Initialize session state
if 'translation_result' not in st.session_state:
    st.session_state.translation_result = None

if 'translation_count' not in st.session_state:
    st.session_state.translation_count = 0

# Header
st.title("🌍 Language Translator")
st.markdown('<p class="subtitle">Translate text instantly between 60+ languages</p>', unsafe_allow_html=True)

# Main layout
col_input, col_settings = st.columns([2, 1])

with col_input:
    st.subheader("📝 Input Text")
    
    input_text = st.text_area(
        "Enter text:",
        height=200,
        placeholder="Type or paste your text here...",
        label_visibility="collapsed"
    )
    
    if input_text:
        char_count = len(input_text)
        word_count = len(input_text.split())
        
        stat_col1, stat_col2 = st.columns(2)
        with stat_col1:
            st.caption(f"📊 **{char_count}** characters")
        with stat_col2:
            st.caption(f"📝 **{word_count}** words")

with col_settings:
    st.subheader("⚙️ Settings")
    
    target_language_name = st.selectbox(
        "Target Language:",
        options=sorted(LANGUAGES.keys()),
        index=sorted(LANGUAGES.keys()).index('Spanish'),
        label_visibility="collapsed"
    )
    
    target_language_code = LANGUAGES[target_language_name]
    
    st.caption(f"🌐 **{target_language_name}**")
    st.caption(f"Code: `{target_language_code}`")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    translate_clicked = st.button(
        "🚀 TRANSLATE NOW",
        type="primary",
        use_container_width=True
    )
    
    clear_clicked = st.button(
        "🗑️ Clear All",
        use_container_width=True
    )

# Handle clear
if clear_clicked:
    st.session_state.translation_result = None
    st.success("✅ Cleared!")
    st.rerun()

# Divider
st.markdown("---")

# Handle translation
if translate_clicked:
    if input_text and input_text.strip():
        with st.spinner(f"🔄 Translating to {target_language_name}..."):
            translated_text = translate_text(input_text, target_language_code)
        
        if translated_text:
            st.session_state.translation_result = {
                'original': input_text,
                'translated': translated_text,
                'target_lang': target_language_name,
                'target_code': target_language_code
            }
            st.session_state.translation_count += 1
            st.success(f"✅ Translated to {target_language_name}!")
        else:
            st.error("❌ Translation failed. Please try again.")
    else:
        st.warning("⚠️ Please enter text to translate.")

# Display result
if st.session_state.translation_result:
    result = st.session_state.translation_result
    
    st.subheader(f"📤 Translation Result")
    
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.caption(f"**From:** Auto-detected")
    with info_col2:
        st.caption(f"**To:** {result['target_lang']}")
    
    st.text_area(
        "Translated:",
        value=result['translated'],
        height=200,
        label_visibility="collapsed"
    )
    
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        if st.button("📋 Show Copy Text", use_container_width=True):
            st.code(result['translated'], language='text')
    
    with action_col2:
        if st.button("🔄 New Translation", use_container_width=True):
            st.session_state.translation_result = None
            st.rerun()
    
    st.markdown("---")
    
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    with stats_col1:
        st.metric("Input", f"{len(result['original'])} chars")
    with stats_col2:
        st.metric("Output", f"{len(result['translated'])} chars")
    with stats_col3:
        st.metric("Total Done", st.session_state.translation_count)

# Sidebar
with st.sidebar:
    st.header("ℹ️ How to Use")
    
    st.markdown("""
    ### Quick Start
    
    1. **Enter Text** 📝
       - Type or paste in the box
    
    2. **Select Language** 🌐
       - Choose from 60+ languages
    
    3. **Translate** 🚀
       - Click "TRANSLATE NOW"
    
    4. **Copy & Use** 📋
       - Click "Show Copy Text"
    
    5. **Start Over** 🔄
       - Use "Clear All" button
    """)
    
    st.markdown("---")
    
    st.info(f"""
    **📊 Statistics**
    - Languages: **{len(LANGUAGES)}**
    - Translations: **{st.session_state.translation_count}**
    - Status: **🟢 Online**
    """)
    
    st.markdown("---")
    
    st.success("""
    **✨ Features**
    - Auto language detection
    - Real-time translation
    - Character counter
    - Copy to clipboard
    - Mobile responsive
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b;'>
    <p>🌐 <strong>Language Translator</strong> | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
