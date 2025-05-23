# streamlit_app/pages/show_images.py

import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Show Uploaded Images", layout="wide")
st.title("🖼️ Uploaded Images for Your Session")
API_BASE = st.secrets["api_base"]


# ✅ Ensure batch_id exists
if "batch_id" not in st.session_state:
    st.error("❌ No batch ID found. Please upload images first from the Home or Upload page.")
    st.stop()

batch_id = st.session_state["batch_id"]

# 🔗 Django API endpoints
LIST_API = f"{API_BASE}/list-images/{batch_id}/"
GET_IMAGE_API = f"{API_BASE}/get-image/"

# 🧠 Fetch list of images from Django
try:
    res = requests.get(LIST_API)
    if res.status_code == 200:
        images = res.json()

        if not images:
            st.info("ℹ️ No images found for this batch ID yet.")
        else:
            st.success(f"✅ {len(images)} images found.")
            cols = st.columns(3)  # Display in a 3-column grid

            for idx, image in enumerate(images):
                file_id = image["file_id"]
                filename = image["filename"]
                image_url = f"{GET_IMAGE_API}{file_id}/"

                # Download image binary
                img_res = requests.get(image_url)
                if img_res.status_code == 200:
                    img = Image.open(BytesIO(img_res.content))
                    with cols[idx % 3]:
                        st.image(img, caption=filename, use_container_width=True)
                else:
                    st.warning(f"⚠️ Failed to load image: {filename}")
    else:
        st.error("🚫 Failed to fetch image list from server.")
except Exception as e:
    st.error(f"🔌 Error fetching images: {e}")
