# streamlit_app/pages/upload_folder.py
import streamlit as st
import zipfile
import requests
import uuid
import io

st.set_page_config(page_title="Upload Folder", layout="wide")
st.title("📁 Upload Folder of Images")

# Generate or reuse batch ID for this session
if "batch_id" not in st.session_state:
    st.session_state["batch_id"] = str(uuid.uuid4())
batch_id = st.session_state["batch_id"]

API_URL = "http://127.0.0.1:8000/api/upload-folder/"

zip_file = st.file_uploader("Upload a ZIP file of images", type=["zip"])

if zip_file is not None:
    if st.button("Upload Images"):
        with zipfile.ZipFile(zip_file, "r") as archive:
            for file_info in archive.infolist():
                if file_info.filename.lower().endswith((".jpg", ".jpeg", ".png")):
                    with archive.open(file_info.filename) as file_data:
                        files = {
                            "image": (file_info.filename, file_data, "image/jpeg")
                        }
                        data = {
                            "batch_id": batch_id
                        }
                        res = requests.post(API_URL, files=files, data=data)
                        if res.status_code != 200:
                            st.error(f"❌ Failed to upload {file_info.filename}")
        st.success(f"✅ All images uploaded from {zip_file.name}")
