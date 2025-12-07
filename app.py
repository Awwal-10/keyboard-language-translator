import streamlit as st
from deep_translator import GoogleTranslator

# Page config - SIMPLE
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="centered"
)

# Get ACTUAL supported languages from the library
try:
    # Use the actual supported languages from GoogleTranslator
    SUPPORTED_LANGUAGES = GoogleTranslator().get_supported_languages(as_dict=True)
    # Convert to proper format: {'English': 'en', 'Spanish': 'es', ...}
    LANGUAGES = {v.title(): k for k, v in SUPPORTED_LANGUAGES.items()}
    LANGUAGES = dict(sorted(LANGUAGES.items()))
except:
    # Fallback to most common languages if there's an error
    LANGUAGES = {
        'English': 'en',
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de',
        'Italian': 'it',
        'Portuguese': 'pt',
        'Russian': 'ru',
        'Japanese': 'ja',
        'Korean': 'ko',
        'Chinese': 'zh-cn',
        'Arabic': 'ar',
        'Hindi': 'hi',
        'Turkish': 'tr',
        'Dutch': 'nl',
        'Greek': 'el',
        'Hebrew': 'he',
        'Swedish': 'sv',
        'Polish': 'pl',
        'Vietnamese': 'vi',
        'Thai': 'th'
    }

def translate_text(text, target_lang):
    """Simple translation function"""
    try:
        if not text or not text.strip():
            return "Please enter text to translate."
        
        # Check if target language is valid
        if target_lang not in LANGUAGES.values():
            return f"Language code '{target_lang}' not supported. Please select a valid language."
        
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
        st.caption(f"Characters: {len(input_text)}")

with col2:
    # Language selection
    st.subheader("Translate to:")
    
    # Search box for languages
    language_search = st.text_input(
        "Search language:",
        placeholder="Type to search...",
        key="search"
    )
    
    # Filter languages based on search
    if language_search:
        filtered_langs = {k: v for k, v in LANGUAGES.items() 
                         if language_search.lower() in k.lower()}
    else:
        filtered_langs = LANGUAGES
    
    # Language dropdown
    target_language_name = st.selectbox(
        "Select language:",
        options=list(filtered_langs.keys()),
        index=1 if 'Spanish' in filtered_langs else 0,
        key="language"
    )
    
    # Get the language code
    target_language_code = LANGUAGES[target_language_name]
    
    # Translate button
    translate_btn = st.button("Translate", type="primary", use_container_width=True)

# Divider
st.markdown("---")

# Translation result
if translate_btn:
    if input_text.strip():
        with st.spinner("Translating..."):
            result = translate_text(input_text, target_language_code)
        
        # Display result
        st.subheader("Translation:")
        st.text_area(
            "Translated text:",
            value=result,
            height=150,
            key="output"
        )
        
        # Simple stats (small and clean)
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Input", f"{len(input_text)} chars")
        with col_b:
            st.metric("Output", f"{len(result)} chars")
            
    else:
        st.warning("Please enter some text to translate.")

# Sidebar info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    **How to use:**
    1. Type text in the box
    2. Select target language
    3. Click Translate
    
    **Features:**
    - 100+ languages
    - Auto language detection
    - Real-time translation
    - Simple interface
    
    **Powered by:**
    - Google Translate API
    - Streamlit
    """)
    
    # Show supported language count
    st.info(f"✅ {len(LANGUAGES)} languages supported")
