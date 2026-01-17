import streamlit as st
from deep_translator import GoogleTranslator

# Page config
st.set_page_config(
    page_title="Language Translator",
    page_icon=None,
    layout="centered"
)

# Global CSS
st.markdown("""
<style>
    .main {
        padding: 2.5rem 1.5rem;
        background: #0b1120;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 900px;
    }

    h1, h2, h3, h4 {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text",
                     "Segoe UI", sans-serif;
        font-weight: 600;
        letter-spacing: 0.02em;
        color: #e5e7eb;
    }

    .subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 0.98rem;
        margin-top: 0.25rem;
        margin-bottom: 2.5rem;
    }

    .stTextArea textarea {
        border-radius: 0.75rem;
        border: 1px solid #1f2933;
        background: #020617;
        color: #e5e7eb;
        font-size: 0.95rem;
    }

    .stTextArea textarea:focus {
        border-color: #1d4ed8;
        box-shadow: 0 0 0 1px #1d4ed8;
    }

    div[data-baseweb="select"] > div {
        background: #020617;
        border-radius: 0.6rem;
        border: 1px solid #1f2933;
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid #111827;
    }

    section[data-testid="stSidebar"] h2 {
        font-size: 1rem;
        color: #e5e7eb;
    }

    hr {
        border: none;
        height: 1px;
        background: radial-gradient(circle, #1f2937 0, transparent 70%);
        margin: 2.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Languages
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

def translate_text(text: str, target_lang: str):
    """Translate text to target language."""
    try:
        if not text or not text.strip():
            return ""
        translator = GoogleTranslator(source="auto", target=target_lang)
        return translator.translate(text.strip()) or ""
    except Exception as e:
        return f"Translation error: {e}"

# Session state for count (optional)
if "translation_count" not in st.session_state:
    st.session_state.translation_count = 0

# Header
st.title("Language Translator")
st.markdown(
    '<p class="subtitle">Clean, minimal interface for fast language translation.</p>',
    unsafe_allow_html=True
)

# Layout
col_input, col_settings = st.columns([2, 1])

with col_input:
    st.subheader("Input")
    input_text = st.text_area(
        "Enter text",
        height=220,
        placeholder="Type or paste your content here...",
        label_visibility="collapsed",
        key="input_text",
    )

    if input_text:
        char_count = len(input_text)
        word_count = len(input_text.split())
        c1, c2 = st.columns(2)
        with c1:
            st.caption(f"{char_count} characters")
        with c2:
            st.caption(f"{word_count} words")

with col_settings:
    st.subheader("Target language")
    target_language_name = st.selectbox(
        "Target language",
        options=sorted(LANGUAGES.keys()),
        index=sorted(LANGUAGES.keys()).index("Spanish"),
        label_visibility="collapsed",
        key="target_lang",
    )
    target_language_code = LANGUAGES[target_language_name]
    st.caption(f"Selected: {target_language_name} ({target_language_code})")

st.markdown("<hr>", unsafe_allow_html=True)

# Auto-translate while typing: recompute each run
translated_text = ""
if input_text and input_text.strip():
    translated_text = translate_text(input_text, target_language_code)
    st.session_state.translation_count += 1

# Result section
st.subheader("Result")
if translated_text:
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.caption("Source: auto-detected")
    with info_col2:
        st.caption(f"Target: {target_language_name}")

    st.text_area(
        "Translated text",
        value=translated_text,
        height=220,
        label_visibility="collapsed",
        key="output_text",
    )
else:
    st.caption("Translation will appear here as you type.")

# Sidebar
with st.sidebar:
    st.header("Overview")
    st.write(
        "Translate text between multiple languages in a minimal interface. "
        "Begin typing to see the translation update."
    )
    st.markdown("---")
    st.subheader("Session")
    st.write(f"Languages available: {len(LANGUAGES)}")
    st.write(f"Translations this session: {st.session_state.translation_count}")
    st.markdown("---")
    st.caption("Built with Python and Streamlit.")
