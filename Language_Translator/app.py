import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile

st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌍",
    layout="centered"
)
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg,
        #667eea 0%,
        #764ba2 25%,
        #6a11cb 50%,
        #2575fc 100%
    );
}

h1 {
    color: white !important;
    text-align: center;
}

h2, h3, label {
    color: white !important;
}

.stTextArea textarea {
    background-color: white !important;
    border-radius: 10px;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: white;
    border-radius: 10px;
}

.stButton button {
    background-color: #ff9800;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    width: 100%;
    height: 50px;
    border: none;
}

.stButton button:hover {
    background-color: #e68900;
}

div[data-testid="stVerticalBlock"] {
    background-color: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)
st.title("🌍 Language Translation Tool")

languages = {
    "English": "en",
    "Tamil": "ta",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Korean": "ko",
    "Arabic": "ar"
}

text = st.text_area(
    "Enter Text",
    height=150,
    placeholder="Type text here..."
)

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox(
        "Source Language",
        list(languages.keys())
    )

with col2:
    target_lang = st.selectbox(
        "Target Language",
        list(languages.keys()),
        index=1
    )

if st.button("Translate"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        try:
            translated_text = GoogleTranslator(
                source=languages[source_lang],
                target=languages[target_lang]
            ).translate(text)

            st.success("Translation Completed!")

            st.subheader("Translated Text")

            st.text_area(
                "",
                value=translated_text,
                height=150
            )

            # Copy Feature
            st.code(translated_text)

            # Text To Speech
            st.subheader("🔊 Listen")

            tts = gTTS(
                text=translated_text,
                lang=languages[target_lang].split('-')[0]
            )

            temp_audio = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp3"
            )

            tts.save(temp_audio.name)

            audio_file = open(temp_audio.name, "rb")
            st.audio(audio_file.read())

        except Exception as e:
            st.error(f"Error: {e}")