import streamlit as st
from deep_translator import GoogleTranslator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure page settings
st.set_page_config(
    page_title="Keyboard Language Translator",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    .output-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .char-counter {
        font-size: 0.8rem;
        color: #666;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

def translate_text(text, target_lang):
    """
    Translate text to target language using GoogleTranslator
    
    Args:
        text (str): Text to translate
        target_lang (str): Target language code (e.g., 'es', 'fr')
    
    Returns:
        str: Translated text or error message
    """
    try:
        if not text.strip():
            return "Please enter some text to translate."
        
        # Initialize translator
        translator = GoogleTranslator(source='auto', target=target_lang)
        
        # Perform translation
        translated_text = translator.translate(text)
        return translated_text
    
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        return f"Translation error: {str(e)}"

def main():
    # Header section
    st.markdown('<div class="main-header">🌐 Keyboard Language Translator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Translate your text in real-time to over 100 languages</div>', unsafe_allow_html=True)
    
    # Supported languages dictionary
    languages = {
        'Spanish': 'es',
        'French': 'fr', 
        'German': 'de',
        'Italian': 'it',
        'Portuguese': 'pt',
        'Russian': 'ru',
        'Japanese': 'ja',
        'Korean': 'ko',
        'Chinese (Simplified)': 'zh-CN',
        'Arabic': 'ar',
        'Hindi': 'hi',
        'Turkish': 'tr',
        'Dutch': 'nl',
        'Greek': 'el',
        'Hebrew': 'iw',
        'English': 'en'
    }
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text input area
        input_text = st.text_area(
            "📝 Enter text to translate:",
            placeholder="Type or paste your text here...",
            height=150,
            key="input_text"
        )
        
        # Character counter
        if input_text:
            char_count = len(input_text)
            st.markdown(f'<div class="char-counter">Characters: {char_count}/5000</div>', unsafe_allow_html=True)
            
            # Warning for long text
            if char_count > 5000:
                st.warning("⚠️ Text is quite long. For better performance, consider breaking it into smaller chunks.")
    
    with col2:
        # Language selection
        st.subheader("🎯 Target Language")
        selected_language = st.selectbox(
            "Choose target language:",
            options=list(languages.keys()),
            index=0,  # Default to Spanish
            key="language_select"
        )
        
        # Display language code
        lang_code = languages[selected_language]
        st.caption(f"Language code: {lang_code}")
        
        # Translate button
        translate_btn = st.button("🚀 Translate", type="primary", use_container_width=True)
    
    # Horizontal line for separation
    st.markdown("---")
    
    # Translation output section
    st.subheader("📤 Translation Result")
    
    # Only translate when button is clicked and there's text
    if translate_btn:
        if input_text.strip():
            with st.spinner("🔄 Translating..."):
                # Perform translation
                translated_text = translate_text(input_text, languages[selected_language])
                
                # Display result in a nice box
                st.markdown('<div class="output-box">', unsafe_allow_html=True)
                st.success("✅ Translation Complete!")
                st.text_area("Translated Text:", value=translated_text, height=150, key="output_text")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Show some stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Input Characters", len(input_text))
                with col2:
                    st.metric("Output Characters", len(translated_text))
                with col3:
                    st.metric("Target Language", selected_language)
        else:
            st.error("❌ Please enter some text to translate.")
    
    # Instructions in sidebar
    with st.sidebar:
        st.header("ℹ️ How to Use")
        st.markdown("""
        1. **Type** your text in the input box
        2. **Select** your target language
        3. **Click** the Translate button
        4. **View** your translated text instantly
        
        ### 🌟 Features
        - Real-time translation
        - 100+ languages supported
        - Character counter
        - Clean, modern interface
        - Error handling
        
        ### ⚠️ Limitations
        - Maximum ~5000 characters
        - Requires internet connection
        - Translation quality depends on Google Translate
        """)
        
        # Add a footer
        st.markdown("---")
        st.markdown("Built with ❤️ using Streamlit & Deep Translator")

if __name__ == "__main__":
    main()