import streamlit as st
from deep_translator import GoogleTranslator

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Language Translator",
    page_icon=None,
    layout="centered"
)

# ---------- GLOBAL STYLES ----------
st.markdown(
    """
<style>
    .main {
        padding: 2.5rem 1.5rem;
        background: #f3f4f6;
    }

    .block-container {
        max-width: 960px;
    }

    h1, h2, h3, h4 {
        font-family: system-ui, -apple-system, BlinkMacSystemFont,
                     "SF Pro Text", "Segoe UI", sans-serif;
        font-weight: 600;
        letter-spacing: 0.01em;
        color: #111827;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 0.95rem;
        margin-top: 0.1rem;
        margin-bottom: 2rem;
    }

    .translator-card {
        background: #ffffff;
        border-radius: 1rem;
        padding: 1.75rem 1.75rem 1.5rem 1.75rem;
        box-shadow:
            0 18px 45px rgba(15, 23, 42, 0.06),
            0 0 0 1px rgba(148, 163, 184, 0.12);
    }

    .stTextArea textarea {
        border-radius: 0.75rem;
        border: 1px solid #d1d5db;
        background: #ffffff;
        color: #111827;
        font-size: 0.95rem;
    }

    .stTextArea textarea:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 1px #2563eb;
    }

    div[data-baseweb="select"] > div {
        background: #ffffff;
        border-radius: 0.75rem;
        border: 1px solid #d1d5db;
        color: #111827;
    }

    .stButton > button {
        background: #2563eb;
        color: #f9fafb;
        border-radius: 999px;
        border: 1px solid #1d4ed8;
        padding: 0.55rem 1.5rem;
        font-size: 0.95rem;
        font-weight: 500;
        cursor: pointer;
        transition: background 0.15s ease, transform 0.08s ease,
                    box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        background: #1d4ed8;
        transform: translateY(-1px);
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.25);
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: none;
    }

    .section-label {
        font-size: 0.86rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        color: #6b7280;
        margin-bottom: 0.35rem;
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(
            to right,
            rgba(209, 213, 219, 0),
            rgba(209, 213, 219, 1),
            rgba(209, 213, 219, 0)
        );
        margin: 1.5rem 0 1.25rem 0;
    }

    .metric-caption {
        color: #6b7280;
        font-size: 0.8rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- LANGUAGE MAP (100 TOTAL) ----------
LANGUAGES = {
    # Existing + additional common languages supported by Google Translate via deep-translator
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Filipino": "tl",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kinyarwanda": "rw",
    "Korean": "ko",
    "Kurdish (Kurmanji)": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Nyanja (Chichewa)": "ny",
    "Odia (Oriya)": "or",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu",
}
# To be safe you can check supported languages with:
# GoogleTranslator().get_supported_languages(as_dict=True)[web:34][web:41]

# ---------- TRANSLATION FUNCTION ----------
def translate_text(text: str, target_lang: str) -> str:
    try:
        if not text or not text.strip():
            return ""
        translator = GoogleTranslator(source="auto", target=target_lang)
        translated = translator.translate(text.strip())
        return translated or ""
    except Exception as e:
        return f"Translation error: {e}"

# ---------- SESSION STATE ----------
if "translation_result" not in st.session_state:
    st.session_state.translation_result = ""
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "translation_count" not in st.session_state:
    st.session_state.translation_count = 0

# ---------- HEADER ----------
st.title("Language Translator")
st.markdown(
    '<p class="subtitle">Type or paste your text, choose a target language, and run a translation when you are ready.</p>',
    unsafe_allow_html=True,
)

# ---------- MAIN CARD ----------
with st.container():
    st.markdown('<div class="translator-card">', unsafe_allow_html=True)

    # Top: input and language settings
    col_input, col_settings = st.columns([2, 1])

    with col_input:
        st.markdown('<div class="section-label">Input</div>', unsafe_allow_html=True)
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
        st.markdown(
            '<div class="section-label">Target language</div>', unsafe_allow_html=True
        )
        sorted_langs = sorted(LANGUAGES.keys())
        default_index = sorted_langs.index("English") if "English" in sorted_langs else 0
        target_language_name = st.selectbox(
            "Target language",
            options=sorted_langs,
            index=default_index,
            label_visibility="collapsed",
            key="target_lang",
        )
        target_language_code = LANGUAGES[target_language_name]
        st.caption(f"Selected: {target_language_name} ({target_language_code})")

        st.markdown("<hr>", unsafe_allow_html=True)

        translate_clicked = st.button("Translate", use_container_width=True)
        clear_clicked = st.button("Clear", use_container_width=True)

    # Clear logic
    if clear_clicked:
        st.session_state.translation_result = ""
        st.session_state.last_input = ""
        st.experimental_rerun()

    # Translate on button click only (faster than on every keystroke)[web:39][web:42]
    if translate_clicked:
        if input_text and input_text.strip():
            with st.spinner(f"Translating to {target_language_name}..."):
                result = translate_text(input_text, target_language_code)
            st.session_state.translation_result = result
            st.session_state.last_input = input_text
            st.session_state.translation_count += 1
        else:
            st.warning("Enter text before starting translation.")

    # Result section
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Result</div>', unsafe_allow_html=True)

    translated_text = st.session_state.translation_result

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

        m1, m2, m3 = st.columns(3)
        with m1:
            if st.session_state.last_input:
                st.caption(
                    f'<span class="metric-caption">Input length</span><br>'
                    f"{len(st.session_state.last_input)} characters",
                    unsafe_allow_html=True,
                )
        with m2:
            if translated_text:
                st.caption(
                    f'<span class="metric-caption">Output length</span><br>'
                    f"{len(translated_text)} characters",
                    unsafe_allow_html=True,
                )
        with m3:
            st.caption(
                f'<span class="metric-caption">Translations this session</span><br>'
                f"{st.session_state.translation_count}",
                unsafe_allow_html=True,
            )
    else:
        st.caption("Run a translation to see the result here.")

    st.markdown("</div>", unsafe_allow_html=True)
