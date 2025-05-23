import streamlit as st
import requests
from moviepy.editor import (
    ImageClip, AudioFileClip, concatenate_videoclips,
    CompositeVideoClip, ColorClip, vfx
)
import tempfile
import os
import random
import imageio_ffmpeg

os.environ["IMAGEIO_FFMPEG_EXE"] = imageio_ffmpeg.get_ffmpeg_exe()


st.set_page_config(page_title="🎬 Preview Video", layout="wide")
st.title("🎞️ Preview Your Video")
API_BASE = st.secrets["api_base"]

# Session Check
if "batch_id" not in st.session_state:
    st.error("❌ No batch ID found.")
    st.stop()

batch_id = st.session_state["batch_id"]
LIST_API = f"{API_BASE}/list-images/{batch_id}/"
GET_IMAGE_API = f"{API_BASE}/get-image/"
GET_AUDIO_API = f"{API_BASE}/get-audio/{batch_id}/"

# Get images
res = requests.get(LIST_API)
if res.status_code != 200:
    st.error("🚫 Failed to fetch images.")
    st.stop()

images_meta = res.json()
if not images_meta:
    st.info("ℹ️ No images found.")
    st.stop()

st.success(f"📸 {len(images_meta)} images found. Choose video options:")

# ------------------- UI Options -------------------
mode = st.radio("Choose Video Mode", ["Normal", "Animated"])
animation_options = []
if mode == "Animated":
    animation_options = st.multiselect(
        "🎨 Choose Animations (will apply sequentially)", 
        ["fadein", "slide_left", "slide_right", "zoom_in", "zoom_out", "grow", "shrink"],
        default=["fadein", "zoom_in"]
    )

if st.button("🎬 Generate Video"):
    # Download images
    image_paths = []
    for img in images_meta:
        file_id = img["file_id"]
        img_res = requests.get(f"{GET_IMAGE_API}{file_id}/")
        if img_res.status_code == 200:
            ext = img["filename"].split(".")[-1]
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}")
            tmp.write(img_res.content)
            tmp.close()
            image_paths.append(tmp.name)

    # Download audio
    audio_res = requests.get(GET_AUDIO_API)
    if audio_res.status_code != 200:
        st.error("🎧 Failed to fetch audio.")
        st.stop()

    audio_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    audio_tmp.write(audio_res.content)
    audio_tmp.close()

    # ------------------- Animation Functions -------------------
    def create_padded_clip(path, duration=3, size=(1080, 720), animation=None):
        base = ImageClip(path).set_duration(duration).resize(height=size[1])
        bg = ColorClip(size=size, color=(0, 0, 0)).set_duration(duration)
        base = base.set_position("center")

        clip = CompositeVideoClip([bg, base])

        # Apply animations
        if animation == "fadein":
            clip = clip.crossfadein(1)
        elif animation == "slide_left":
            clip = base.set_position(lambda t: ('center', int(size[1] * (1 - t / duration))))
            clip = CompositeVideoClip([bg, clip])
        elif animation == "slide_right":
            clip = base.set_position(lambda t: ('center', int(-size[1] * (1 - t / duration))))
            clip = CompositeVideoClip([bg, clip])
        elif animation == "zoom_in":
            clip = clip.fx(vfx.resize, lambda t: 1 + 0.1 * t)
        elif animation == "zoom_out":
            clip = clip.fx(vfx.resize, lambda t: 1.2 - 0.1 * t)
        elif animation == "grow":
            clip = base.set_start(0).fx(vfx.resize, lambda t: 0.2 + 0.8 * (t / duration))
            clip = CompositeVideoClip([bg, clip])
        elif animation == "shrink":
            clip = base.set_start(0).fx(vfx.resize, lambda t: 1.2 - 0.6 * (t / duration))
            clip = CompositeVideoClip([bg, clip])

        return clip

    # ------------------- Build Video -------------------
    duration = 3
    clips = []
    for i, path in enumerate(image_paths):
        if mode == "Normal":
            clip = create_padded_clip(path, duration)
        else:
            animation = animation_options[i % len(animation_options)] if animation_options else None
            clip = create_padded_clip(path, duration, animation=animation)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")
    audio = AudioFileClip(audio_tmp.name)
    final_video = video.set_audio(audio)

    # Export
    video_path = os.path.join(tempfile.gettempdir(), f"{batch_id}_final_video.mp4")
    final_video.write_videofile(video_path, fps=24)

    with open(video_path, "rb") as f:
        st.video(f.read())
        st.download_button("⬇️ Download Final Video", f, file_name="final_video.mp4")

# ✅ Clean up
st.title("✅ Final Step: Clean Up Session Data")
if st.button("Finished"):
    DELETE_URL = f"{API_BASE}/delete-batch/{batch_id}/"
    res = requests.delete(DELETE_URL)
    if res.status_code == 200:
        st.success(f"Batch {batch_id} deleted.")
        del st.session_state["batch_id"]
    else:
        st.error("Failed to delete batch.")
