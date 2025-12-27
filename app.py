import streamlit as st
from deep_translator import GoogleTranslator
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 2rem 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Title styling */
    h1 {
        color: #1e40af;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 16px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%);
        box-shadow: 0 6px 12px rgba(37, 99, 235, 0.3);
        transform: translateY(-2px);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border: 2px solid #dbeafe;
        border-radius: 12px;
        font-size: 16px;
        padding: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* Select box styling */
    div[data-baseweb="select"] > div {
        border: 2px solid #dbeafe;
        border-radius: 10px;
        transition: border-color 0.3s ease;
    }
    
    div[data-baseweb="select"]:focus-within > div {
        border-color: #2563eb;
    }
    
    /* Success/warning boxes */
    .stSuccess, .stWarning, .stInfo {
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Divider styling */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #dbeafe, transparent);
        margin: 2rem 0;
    }
    
    /* Caption styling */
    .stCaption {
        color: #64748b;
        font-size: 0.875rem;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* Card-like containers */
    .translation-card {
        background: #ffffff;
        border: 2px solid #dbeafe;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# ==================== LANGUAGE DICTIONARY ====================
# Comprehensive language list with proper display names
LANGUAGES = {
    'Afrikaans': 'af',
    'Albanian': 'sq',
    'Amharic': 'am',
    'Arabic': 'ar',
    'Armenian': 'hy',
    'Azerbaijani': 'az',
    'Basque': 'eu',
    'Belarusian': 'be',
    'Bengali': 'bn',
    'Bosnian': 'bs',
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
    'Gujarati': 'gu',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Kannada': 'kn',
    'Korean': 'ko',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Macedonian': 'mk',
    'Malay': 'ms',
    'Malayalam': 'ml',
    'Marathi': 'mr',
    'Norwegian': 'no',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Punjabi': 'pa',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Serbian': 'sr',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Spanish': 'es',
    'Swahili': 'sw',
    'Swedish': 'sv',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Thai': 'th',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Vietnamese': 'vi',
    'Welsh': 'cy'
}

# ==================== TRANSLATION FUNCTION ====================
def translate_text(text, target_lang):
    """
    Translate text to target language using Google Translate
    
    Args:
        text (str): Text to translate
        target_lang (str): Target language code (e.g., 'es', 'fr')
    
    Returns:
        str: Translated text or error message
    """
    try:
        # Validate input
        if not text or not text.strip():
            return "⚠️ Please enter text to translate."
        
        # Create translator instance with auto-detection
        translator = GoogleTranslator(source='auto', target=target_lang)
        
        # Perform translation
        result = translator.translate(text.strip())
        
        return result if result else "Translation failed. Please try again."
    
    except Exception as e:
        error_msg = str(e)
        if "target language" in error_msg.lower():
            return "❌ Invalid target language selected."
        elif "connection" in error_msg.lower() or "network" in error_msg.lower():
            return "❌ Network error. Please check your connection."
        else:
            return f"❌ Translation error: {error_msg}"

# ==================== SESSION STATE INITIALIZATION ====================
# Initialize all session state variables
if 'translation_result' not in st.session_state:
    st.session_state.translation_result = None

if 'last_input_text' not in st.session_state:
    st.session_state.last_input_text = ""

if 'last_target_lang' not in st.session_state:
    st.session_state.last_target_lang = "Spanish"

if 'translation_count' not in st.session_state:
    st.session_state.translation_count = 0

# ==================== HEADER ====================
st.title("🌍 Language Translator")
st.markdown('<p class="subtitle">Translate text instantly between 60+ languages</p>', unsafe_allow_html=True)

# ==================== MAIN LAYOUT ====================
# Create two-column layout for input and settings
col_input, col_settings = st.columns([2, 1])

with col_input:
    st.subheader("📝 Input Text")
    
    # Input text area
    input_text = st.text_area(
        "Enter text to translate:",
        height=200,
        placeholder="Type or paste your text here...",
        key="input_area",
        label_visibility="collapsed"
    )
    
    # Character counter with visual feedback
    if input_text:
        char_count = len(input_text)
        word_count = len(input_text.split())
        
        # Create columns for stats
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        with stat_col1:
            st.caption(f"📊 **{char_count}** characters")
        with stat_col2:
            st.caption(f"📝 **{word_count}** words")
        with stat_col3:
            # Color code based on length
            if char_count > 5000:
                st.caption("⚠️ **Long text**")
            else:
                st.caption("✅ **Ready**")

with col_settings:
    st.subheader("⚙️ Settings")
    
    # Language selector with proper display names
    target_language_name = st.selectbox(
        "Target Language:",
        options=sorted(LANGUAGES.keys()),  # Sort alphabetically
        index=sorted(LANGUAGES.keys()).index('Spanish'),  # Default to Spanish
        key="language_selector",
        label_visibility="collapsed"
    )
    
    # Get the language code
    target_language_code = LANGUAGES[target_language_name]
    
    # Display language info
    st.caption(f"🌐 Language: **{target_language_name}**")
    st.caption(f"💻 Code: `{target_language_code}`")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Translate button
    translate_clicked = st.button(
        "🚀 TRANSLATE NOW",
        type="primary",
        use_container_width=True,
        disabled=not input_text  # Disable if no input
    )
    
    # Clear button
    clear_clicked = st.button(
        "🗑️ Clear All",
        use_container_width=True
    )
    
    # Quick language buttons
    st.markdown("---")
    st.caption("**Quick Select:**")
    
    quick_langs = ['Spanish', 'French', 'German', 'Chinese (Simplified)', 'Japanese']
    for lang in quick_langs:
        if st.button(f"→ {lang}", use_container_width=True, key=f"quick_{lang}"):
            st.session_state.language_selector = lang
            st.rerun()

# ==================== HANDLE CLEAR BUTTON ====================
if clear_clicked:
    # Reset all session state
    st.session_state.translation_result = None
    st.session_state.last_input_text = ""
    st.session_state.input_area = ""
    st.success("✅ Cleared! Ready for new translation.")
    time.sleep(0.5)
    st.rerun()

# ==================== DIVIDER ====================
st.markdown("---")

# ==================== HANDLE TRANSLATION ====================
if translate_clicked:
    if input_text and input_text.strip():
        # Show loading spinner
        with st.spinner(f"🔄 Translating to {target_language_name}..."):
            # Perform translation
            translated_text = translate_text(input_text, target_language_code)
            
            # Simulate slight delay for UX (optional)
            time.sleep(0.3)
        
        # Store result in session state
        st.session_state.translation_result = {
            'original': input_text,
            'translated': translated_text,
            'source_lang': 'Auto-detected',
            'target_lang': target_language_name,
            'target_code': target_language_code,
            'timestamp': time.strftime("%I:%M %p")
        }
        
        # Update tracking
        st.session_state.last_input_text = input_text
        st.session_state.last_target_lang = target_language_name
        st.session_state.translation_count += 1
        
        # Show success message
        st.success(f"✅ Translation complete! Translated to {target_language_name}")
    else:
        st.warning("⚠️ Please enter text to translate.")

# ==================== DISPLAY TRANSLATION RESULT ====================
if st.session_state.translation_result:
    result = st.session_state.translation_result
    
    # Create result section
    st.subheader(f"📤 Translation Result")
    
    # Show translation info
    info_col1, info_col2, info_col3 = st.columns(3)
    with info_col1:
        st.caption(f"**From:** {result['source_lang']}")
    with info_col2:
        st.caption(f"**To:** {result['target_lang']}")
    with info_col3:
        st.caption(f"**Time:** {result['timestamp']}")
    
    # Display translated text
    st.text_area(
        "Translated Text:",
        value=result['translated'],
        height=200,
        key="output_area",
        label_visibility="collapsed"
    )
    
    # Action buttons
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        # Copy button (shows the text in a code block for easy copying)
        if st.button("📋 Show Copy Text", use_container_width=True):
            st.code(result['translated'], language='text')
            st.info("👆 Select and copy the text above")
    
    with action_col2:
        # New translation button
        if st.button("🔄 New Translation", use_container_width=True):
            st.session_state.translation_result = None
            st.session_state.input_area = ""
            st.rerun()
    
    # Statistics
    st.markdown("---")
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    with stats_col1:
        st.metric("Input Length", f"{len(result['original'])} chars")
    
    with stats_col2:
        st.metric("Output Length", f"{len(result['translated'])} chars")
    
    with stats_col3:
        st.metric("Total Translations", st.session_state.translation_count)

# ==================== SIDEBAR ====================
with st.sidebar:
    st.header("ℹ️ How to Use")
    
    st.markdown("""
    ### Quick Start Guide
    
    1. **Enter Text** 📝
       - Type or paste text in the input box
       - Monitor character and word count
    
    2. **Select Language** 🌐
       - Choose from 60+ languages
       - Use dropdown or quick buttons
    
    3. **Translate** 🚀
       - Click "TRANSLATE NOW"
       - Wait for instant results
    
    4. **Copy & Use** 📋
       - Click "Show Copy Text"
       - Copy the translated text
    
    5. **Start Over** 🔄
       - Use "Clear All" to reset
       - Or "New Translation" for another
    """)
    
    st.markdown("---")
    
    st.info(f"""
    **📊 App Statistics**
    - Languages Available: **{len(LANGUAGES)}**
    - Translations Today: **{st.session_state.translation_count}**
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
    - Clean interface
    """)
    
    st.markdown("---")
    
    st.warning("""
    **💡 Tips**
    - Shorter text = faster results
    - Check for typos first
    - Use clear, simple language
    - Translations are powered by Google
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 1rem;'>
    <p>🌐 <strong>Language Translator</strong> | Built with Streamlit & Google Translate</p>
    <p style='font-size: 0.875rem;'>Professional translation tool for instant language conversion</p>
</div>
""", unsafe_allow_html=True)
