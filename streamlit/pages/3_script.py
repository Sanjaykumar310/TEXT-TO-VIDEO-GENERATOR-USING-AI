import streamlit as st
from gtts import gTTS
from io import BytesIO
import requests
from mutagen.mp3 import MP3

st.set_page_config(page_title="Script to Audio", layout="wide")
st.title("📝 Write Your Script")
API_BASE ="http://127.0.0.1:8000/api"

# ✅ Ensure session data is available
if "video_duration" not in st.session_state or "batch_id" not in st.session_state:
    st.error("⚠️ Missing session data. Please complete the previous steps.")
    st.stop()

duration = st.session_state["video_duration"]
batch_id = st.session_state["batch_id"]
word_limit = 100 if duration == "1 minute" else 200

st.info(f"✍️ Please write a script of approximately **{word_limit} words** for your {duration} video.")

script_text = st.text_area("🗒️ Enter your script below:", height=word_limit)

if st.button("📤 Save Script & Upload Audio"):
    if not script_text.strip():
        st.warning("⚠️ Script is empty. Please write something.")
        st.stop()

    try:
        # ✅ Convert script to audio (MP3) in-memory using gTTS + BytesIO
        tts = gTTS(text=script_text, lang='en')
        audio_io = BytesIO()
        tts.write_to_fp(audio_io)
        audio_io.seek(0)

        try:
            # ✅ Get audio duration using mutagen (no ffmpeg required)
            audio_bytes = audio_io.getvalue()
            audio_file_like = BytesIO(audio_bytes)
            audio = MP3(audio_file_like)
            duration_sec = audio.info.length
            st.success(f"✅ Audio generated, length: {duration_sec:.2f} seconds")
        except Exception as e:
            st.error(f"❌ gTTS generated invalid audio: {e}")
            st.stop()

        audio_io.seek(0)  # 🔁 rewind AGAIN before upload

        # ✅ Upload to Django backend
        files = {
            "audio": ("script.mp3", audio_io, "audio/mpeg")
        }
        data = {
            "script": script_text,
            "duration": duration,
            "batch_id": batch_id
        }

        res = requests.post(f"{API_BASE}/save-script/", files=files, data=data)

        if res.status_code == 200:
            st.success("✅ Script and audio successfully uploaded!")
        else:
            st.error(f"❌ Upload failed: {res.status_code} - {res.text}")

    except Exception as e:
        st.error(f"🚫 Error during audio generation or upload: {e}")
