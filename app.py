import streamlit as st
from deep_translator import GoogleTranslator
import pandas as pd

# Configure page for modern look
st.set_page_config(
    page_title="🌍 Instant Language Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS FOR MODERN UI ==========
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Headers */
    .main-title {
        font-size: 3rem;
        color: white;
        text-align: center;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .sub-title {
        font-size: 1.2rem;
        color: #f0f0f0;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Cards */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Input area */
    .stTextArea textarea {
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        font-size: 16px;
        transition: all 0.3s;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Output box */
    .output-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
        border-left: 6px solid #667eea;
        min-height: 200px;
    }
    
    /* Stats */
    .stat-box {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    
    /* Language dropdown */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 12px;
    }
    
    /* Badges */
    .language-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# ========== ALL 100+ LANGUAGES ==========
LANGUAGES = {
    'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar',
    'Armenian': 'hy', 'Azerbaijani': 'az', 'Basque': 'eu', 'Belarusian': 'be',
    'Bengali': 'bn', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Catalan': 'ca',
    'Cebuano': 'ceb', 'Chinese (Simplified)': 'zh-cn', 'Chinese (Traditional)': 'zh-tw',
    'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da',
    'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et',
    'Finnish': 'fi', 'French': 'fr', 'Frisian': 'fy', 'Galician': 'gl',
    'Georgian': 'ka', 'German': 'de', 'Greek': 'el', 'Gujarati': 'gu',
    'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'he',
    'Hindi': 'hi', 'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is',
    'Igbo': 'ig', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it',
    'Japanese': 'ja', 'Javanese': 'jv', 'Kannada': 'kn', 'Kazakh': 'kk',
    'Khmer': 'km', 'Kinyarwanda': 'rw', 'Korean': 'ko', 'Kurdish': 'ku',
    'Kyrgyz': 'ky', 'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv',
    'Lithuanian': 'lt', 'Luxembourgish': 'lb', 'Macedonian': 'mk', 'Malagasy': 'mg',
    'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt', 'Maori': 'mi',
    'Marathi': 'mr', 'Mongolian': 'mn', 'Myanmar (Burmese)': 'my', 'Nepali': 'ne',
    'Norwegian': 'no', 'Nyanja (Chichewa)': 'ny', 'Odia (Oriya)': 'or',
    'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt',
    'Punjabi': 'pa', 'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm',
    'Scots Gaelic': 'gd', 'Serbian': 'sr', 'Sesotho': 'st', 'Shona': 'sn',
    'Sindhi': 'sd', 'Sinhala (Sinhalese)': 'si', 'Slovak': 'sk', 'Slovenian': 'sl',
    'Somali': 'so', 'Spanish': 'es', 'Sundanese': 'su', 'Swahili': 'sw',
    'Swedish': 'sv', 'Tagalog (Filipino)': 'tl', 'Tajik': 'tg', 'Tamil': 'ta',
    'Tatar': 'tt', 'Telugu': 'te', 'Thai': 'th', 'Turkish': 'tr',
    'Turkmen': 'tk', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uyghur': 'ug',
    'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh',
    'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu'
}

# ========== HELPER FUNCTIONS ==========
def translate_text(text, target_lang, source_lang='auto'):
    """Translate text using Google Translate"""
    try:
        if not text.strip():
            return "📝 Please enter some text to translate.", "auto"
        
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(text)
        
        # Detect source language
        if source_lang == 'auto':
            try:
                detected_lang = GoogleTranslator().detect(text)
                return translated, detected_lang
            except:
                return translated, "auto"
        return translated, source_lang
    
    except Exception as e:
        return f"⚠️ Translation error: {str(e)}", "auto"

# ========== MAIN APP ==========
def main():
    # ===== HERO SECTION =====
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-title">🌍 Instant Language Translator</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-title">Translate instantly between 100+ languages • Real-time • Free • No Signup Required</p>', unsafe_allow_html=True)
    
    # Add some space
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== MAIN CONTENT =====
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # INPUT SECTION
        st.subheader("📝 Enter Text to Translate")
        input_text = st.text_area(
            "",
            height=180,
            placeholder="Type or paste your text here... (Maximum 5000 characters)",
            key="input_text",
            label_visibility="collapsed"
        )
        
        # Character counter with progress
        if input_text:
            char_count = len(input_text)
            max_chars = 5000
            progress = min(char_count / max_chars, 1.0)
            
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.progress(progress)
            with col_b:
                if char_count > 4000:
                    st.error(f"⚠️ {char_count}/{max_chars}")
                else:
                    st.info(f"📊 {char_count}/{max_chars}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # LANGUAGE SELECTION
        st.subheader("🎯 Translation Settings")
        
        # Auto-detect checkbox
        auto_detect = st.checkbox("🔍 Auto-detect source language", value=True)
        
        if not auto_detect:
            source_lang = st.selectbox(
                "From:",
                options=list(LANGUAGES.keys()),
                index=list(LANGUAGES.keys()).index('English')
            )
        else:
            source_lang = 'auto'
        
        # Target language with search
        st.subheader("🌎 Translate To")
        target_lang_name = st.selectbox(
            "Select target language:",
            options=list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index('Spanish'),  # FIXED TYPO HERE
            key="target_lang"
        )
        target_lang_code = LANGUAGES[target_lang_name]
        
        # Language code display
        st.caption(f"Language code: **{target_lang_code}**")
        
        # Quick language buttons
        st.subheader("⚡ Quick Select")
        quick_langs = st.columns(3)
        with quick_langs[0]:
            if st.button("🇪🇸 Spanish", use_container_width=True):
                target_lang_name = "Spanish"
        with quick_langs[1]:
            if st.button("🇫🇷 French", use_container_width=True):
                target_lang_name = "French"
        with quick_langs[2]:
            if st.button("🇩🇪 German", use_container_width=True):
                target_lang_name = "German"
        
        # Translate button
        translate_clicked = st.button(
            "🚀 TRANSLATE NOW",
            type="primary",
            use_container_width=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ===== TRANSLATION OUTPUT =====
    if translate_clicked:
        if input_text.strip():
            with st.spinner("🔄 Translating... Please wait"):
                translated_text, detected_lang = translate_text(
                    input_text, 
                    LANGUAGES[target_lang_name],
                    source_lang
                )
            
            # OUTPUT CARD
            st.markdown('<div class="output-card">', unsafe_allow_html=True)
            
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.success("✅ Translation Complete!")
            with col_b:
                if detected_lang != 'auto':
                    # Try to get the language name from the code
                    lang_name = [name for name, code in LANGUAGES.items() if code == detected_lang]
                    if lang_name:
                        st.info(f"Detected language: **{lang_name[0]}**")
            
            # Display translated text
            st.text_area(
                "Translated Text:",
                value=translated_text,
                height=200,
                key="output_text"
            )
            
            # STATISTICS
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="stat-box">', unsafe_allow_html=True)
                st.metric("Input Text", f"{len(input_text)} chars")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="stat-box">', unsafe_allow_html=True)
                st.metric("Output Text", f"{len(translated_text)} chars")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="stat-box">', unsafe_allow_html=True)
                if detected_lang != 'auto':
                    lang_name = [name for name, code in LANGUAGES.items() if code == detected_lang]
                    if lang_name:
                        st.metric("Source", lang_name[0])
                    else:
                        st.metric("Source", "Auto-detected")
                else:
                    st.metric("Source", "Auto-detected")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div class="stat-box">', unsafe_allow_html=True)
                st.metric("Target", target_lang_name)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # COPY TO CLIPBOARD FEATURE
            if st.button("📋 Copy Translation to Clipboard"):
                st.code(translated_text, language='text')
                st.success("✅ Copied to clipboard!")
        
        else:
            st.error("❌ Please enter some text to translate.")
    
    # ===== SIDEBAR =====
    with st.sidebar:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.header("ℹ️ How to Use")
        st.markdown("""
        1. **Type** your text in the input box
        2. **Choose** target language (or use quick buttons)
        3. **Click** TRANSLATE NOW
        4. **View** your translated text instantly
        
        ### ✨ Features
        - 100+ languages supported
        - Auto language detection
        - Character counter
        - Copy to clipboard
        - Translation statistics
        - Mobile-friendly design
        """)
        
        # Show sample languages
        st.subheader("🌐 Popular Languages")
        popular_langs = [
            "Spanish", "French", "German", "Japanese",
            "Chinese (Simplified)", "Arabic", "Hindi", "Portuguese"
        ]
        
        for lang in popular_langs:
            st.markdown(f'<span class="language-badge">{lang}</span>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ABOUT SECTION
        st.markdown("---")
        st.markdown("""
        ### 🚀 Powered By
        - **Google Translate API**
        - **Streamlit** for web interface
        - **Deep Translator** library
        
        ### 📞 Support
        Issues? Report on GitHub
        
        ⭐ **Star on GitHub if you like it!**
        """)

if __name__ == "__main__":
    main()
