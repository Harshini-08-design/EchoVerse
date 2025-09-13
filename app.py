import streamlit as st
from transformers import pipeline
from gtts import gTTS
import subprocess
import os
from pathlib import Path
from deep_translator import GoogleTranslator

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>
    /* Whole App Background */
    .stApp {
        background: linear-gradient(135deg, #ffecd2, #fcb69f, #ffdde1, #c2e9fb) !important;
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: "Poppins", sans-serif;
        color: #222 !important;
    }

    /* Gradient Animation */
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Title */
    h1 {
        text-align: center;
        font-size: 50px !important;
        color: #ffffff !important;
        background: linear-gradient(90deg, #ff6a00, #ee0979, #00c6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        margin-bottom: 30px;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        border: 3px dashed #ff6a00 !important;
        background: #fff5f5 !important;
        border-radius: 15px;
        padding: 20px;
        transition: 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border: 3px dashed #87CEFA !important;
        background: #eefaff !important;
        transition: all 0.3s ease-in-out;
    }

    /* Browse Files Button inside FileUploader */
    [data-testid="stFileUploader"] button {
        background: linear-gradient(90deg, #ff6a00, #ee0979, #00c6ff) !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 15px !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 8px 16px !important;
        cursor: pointer !important;
        transition: all 0.3s ease-in-out !important;
    }

    /* Hover Effect for Browse Button */
    [data-testid="stFileUploader"] button:hover {
        background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
        transform: scale(1.05);
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }

    /* Text Area */
    [data-testid="stTextArea"] textarea {
        border: 3px solid #80dfff !important;
        border-radius: 15px !important;
        background: #ffffff !important;
        color: #4f92f8 !important;
        font-size: 16px !important;
        padding: 15px !important;
    }

    /* Dropdowns */
    [data-testid="stSelectbox"] div[role="combobox"] {
        border: 3px solid #80dfff !important;
        border-radius: 12px !important;
        background: #ffffff !important;
        padding: 8px !important;
        font-size: 16px !important;
    }
    /* Make form labels bold */
    [data-testid="stTextArea"] label,
    [data-testid="stSelectbox"] label {
        font-weight: bold !important;
        font-size: 18px !important;
        color: #222 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #ff6a00, #ee0979, #00c6ff);
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        cursor: pointer !important;
        transition: all 0.3s ease-in-out !important;
    }
    .stButton > button:hover {
        transform: scale(1.08);
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }

    /* Audio player */
    .stAudio {
        border: 3px solid #00c6ff !important;
        border-radius: 15px !important;
        background: #e6f7ff !important;
        padding: 10px;
    }

    /* Info & Warnings */
    .stAlert {
        border-radius: 12px !important;
        font-size: 16px !important;
    }
    /* Style all labels */
    .stMarkdown p {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #0b0000 !important;
        margin-bottom: 8px !important;
    }

    /* OR more specific targeting */
    [data-testid="stTextArea"] label,
    [data-testid="stSelectbox"] label {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #000102 !important;
    }
    
    /* Custom card for text sections */
    .text-card {
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 15px 0;
        border: 2px solid #80dfff;
    }
    
    /* Download button */
    .stDownloadButton button {
        background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
    }
    
    .stDownloadButton button:hover {
        background: linear-gradient(90deg, #0072ff, #0052cc) !important;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Setup
# ----------------------------
st.set_page_config(page_title="EchoVerse", layout="wide", page_icon="🎧")
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

# Language options with codes for gTTS
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Hindi": "hi",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese (Simplified)": "zh-cn",
    "Arabic": "ar",
    "Russian": "ru",
    "Dutch": "nl",
    "Turkish": "tr",
    "Greek": "el",
    "Swedish": "sv",
    "Norwegian": "no",
    "Danish": "da",
    "Finnish": "fi",
    "Polish": "pl",
    "Romanian": "ro",
    "Indonesian": "id",
    "Malay": "ms",
    "Thai": "th",
    "Vietnamese": "vi",
    "Czech": "cs",
    "Hungarian": "hu",
    "Catalan": "ca",
    "Ukrainian": "uk",
    "Bulgarian": "bg",
    "Croatian": "hr",
    "Slovak": "sk",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
    "Persian": "fa",
    "Hebrew": "he"
}

# Language-specific tone instructions
TONE_INSTRUCTIONS = {
    "English": {
        "Neutral": "Rewrite the following text in a clear, neutral tone while preserving all facts:",
        "Suspenseful": "Rewrite the following text in a suspenseful, mysterious tone that builds tension:",
        "Inspiring": "Rewrite the following text in an inspiring, motivational tone that uplifts the reader:",
        "Professional": "Rewrite the following text in a formal, professional tone suitable for business:",
        "Casual": "Rewrite the following text in a casual, friendly tone as if talking to a friend:",
        "Friendly": "Rewrite the following text in a warm, friendly tone:",
        "Formal": "Rewrite the following text in a very formal, academic tone:"
    },
    "Spanish": {
        "Neutral": "Reescribe el siguiente texto en un tono claro y neutral preservando todos los hechos:",
        "Suspenseful": "Reescribe el siguiente texto en un tono misterioso y de suspenso que genere tensión:",
        "Inspiring": "Reescribe el siguiente texto en un tono inspirador y motivador que eleve al lector:",
        "Professional": "Reescribe el siguiente texto en un tono formal y profesional adecuado para negocios:",
        "Casual": "Reescribe el siguiente texto en un tono casual y amigable como si hablaras con un amigo:"
    },
    "French": {
        "Neutral": "Réécrivez le texte suivant dans un ton clair et neutre en préservant tous les faits:",
        "Suspenseful": "Réécrivez le texte suivant dans un ton mystérieux et suspensif qui crée de la tension:",
        "Inspiring": "Réécrivez le texte suivant dans un ton inspirant et motivant qui élève le lecteur:",
        "Professional": "Réécrivez le texte suivant dans un ton formel et professionnel adapté aux affaires:",
        "Casual": "Réécrivez le texte suivant dans un ton décontracté et amical comme si vous parliez à un ami:"
    },
    "German": {
        "Neutral": "Schreiben Sie den folgenden Text in einem klaren, neutralen Ton um und bewahren Sie alle Fakten:",
        "Suspenseful": "Schreiben Sie den folgenden Text in einem spannenden, mysteriösen Ton um, der Spannung aufbaut:",
        "Inspiring": "Schreiben Sie den folgenden Text in einem inspirierenden, motivierenden Ton um, der den Leser erhebt:",
        "Professional": "Schreiben Sie den folgenden Text in einem formalen, professionellen Ton um, der für geschäftliche Zwecke geeignet ist:",
        "Casual": "Schreiben Sie den folgenden Text in einem lockeren, freundlichen Ton um, als ob Sie mit einem Freund sprechen würden:"
    }
}

# Default instructions for languages not in the dictionary
DEFAULT_INSTRUCTIONS = {
    "Neutral": "Rewrite the following text in a clear, neutral tone while preserving all facts:",
    "Suspenseful": "Rewrite the following text in a suspenseful, mysterious tone that builds tension:",
    "Inspiring": "Rewrite the following text in an inspiring, motivational tone that uplifts the reader:",
    "Professional": "Rewrite the following text in a formal, professional tone suitable for business:",
    "Casual": "Rewrite the following text in a casual, friendly tone as if talking to a friend:",
    "Friendly": "Rewrite the following text in a warm, friendly tone:",
    "Formal": "Rewrite the following text in a very formal, academic tone:"
}

# Load Hugging Face model for rewriting text
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-base")

rewrite_model = load_model()

# ----------------------------
# Helper functions
# ----------------------------
def rewrite_text(text, tone, language="English"):
    # Get the appropriate instruction based on language
    if language in TONE_INSTRUCTIONS and tone in TONE_INSTRUCTIONS[language]:
        instruction = TONE_INSTRUCTIONS[language][tone]
    else:
        instruction = DEFAULT_INSTRUCTIONS.get(tone, DEFAULT_INSTRUCTIONS["Neutral"])
    
    prompt = f"{instruction}\n\n{text}"
    result = rewrite_model(prompt, max_length=512, num_return_sequences=1)
    return result[0]["generated_text"]

def translate_text(text, target_lang):
    """Translate text to the target language"""
    if target_lang == "English":
        return text  # No translation needed for English
    
    try:
        lang_code = LANGUAGES[target_lang]
        translated = GoogleTranslator(source='auto', target=lang_code).translate(text)
        return translated
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text  # Return original text if translation fails

def text_to_speech(text, lang_code, filename="output.mp3"):
    # Use gTTS to create speech
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        mp3_file = output_dir / filename
        tts.save(str(mp3_file))
        return mp3_file
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("🎧 EchoVerse – AI-Powered Audiobook Creator")

st.markdown("""
<div style='background-color: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 15px; border-left: 5px solid #00c6ff;'>
    <p style='font-size: 18px; margin: 0; color: #222;'>Upload text or paste below, choose language, tone and voice, then generate expressive audio narration.</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 Input")
    uploaded_file = st.file_uploader("Upload a .txt file", type="txt")
    user_text = st.text_area("Or paste your text here:", height=200, placeholder="Enter your text here...")

if uploaded_file:
    user_text = uploaded_file.read().decode("utf-8")

with col2:
    st.markdown("### ⚙️ Settings")
    
    # Language selection
    selected_language = st.selectbox(
        "Choose Language for Audio", 
        options=list(LANGUAGES.keys()),
        index=0,  # Default to English
        help="Select the language you want the audio to be generated in"
    )
    
    # Tone selection
    if selected_language in TONE_INSTRUCTIONS:
        tone_options = list(TONE_INSTRUCTIONS[selected_language].keys())
    else:
        tone_options = list(DEFAULT_INSTRUCTIONS.keys())
    
    tone = st.selectbox("Choose tone", tone_options)
    
    # Voice selection (placeholder for future expansion)
    voice = st.selectbox("Choose voice", ["Default"])

# Center the generate button
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_btn = st.button("🎵 Generate Audiobook", use_container_width=True)

if generate_btn:
    if user_text.strip():
        # Create two columns for original and rewritten text
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='text-card'>", unsafe_allow_html=True)
            st.subheader("📄 Original Text")
            st.write(user_text)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Rewrite with tone
        with st.spinner(f"✨ Rewriting text in {tone} tone..."):
            rewritten = rewrite_text(user_text, tone, selected_language)
        
        # Translate to target language if needed
        if selected_language != "English":
            with st.spinner(f"🌍 Translating to {selected_language}..."):
                rewritten = translate_text(rewritten, selected_language)
        
        with col2:
            st.markdown("<div class='text-card'>", unsafe_allow_html=True)
            st.subheader(f"🎭 {tone} Version ({selected_language})")
            st.write(rewritten)
            st.markdown("</div>", unsafe_allow_html=True)

        # Generate speech in the selected language
        lang_code = LANGUAGES[selected_language]
        with st.spinner(f"🔊 Generating {selected_language} audio..."):
            audio_file = text_to_speech(rewritten, lang_code, "audiobook.mp3")

        if audio_file:
            # Audio player
            st.markdown(f"### 🔊 {selected_language} Audio Preview")
            st.audio(str(audio_file), format="audio/mp3")

            # Download button
            with open(audio_file, "rb") as f:
                st.download_button(
                    label="📥 Download MP3",
                    data=f,
                    file_name=f"echoverse_{selected_language.lower()}_{tone.lower()}.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )
    else:
        st.warning("⚠️ Please provide some text first!")