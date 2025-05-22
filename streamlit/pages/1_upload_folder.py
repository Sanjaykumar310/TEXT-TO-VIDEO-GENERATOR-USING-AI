import streamlit as st
import zipfile
import requests

st.set_page_config(page_title="Upload Folder", layout="wide")
st.title("📁 Upload Folder of Images")

batch_id = st.session_state.get("batch_id")

API_URL = "http://127.0.0.1:8000/api/upload-folder/"

# Track upload state
if "has_uploaded" not in st.session_state:
    st.session_state["has_uploaded"] = False

selected_time = st.radio("⏱️ Select the video duration", ["1 minute", "2 minutes"])
st.session_state["video_duration"] = selected_time


# Required number of images
required_images = 22 if selected_time == "1 minute" else 44
st.info(f"📷 Please upload exactly **{required_images} images** for a {selected_time} video.")

# 2️⃣ File Uploader
zip_file = st.file_uploader("Upload a ZIP file of images", type=["zip"])

if st.session_state["has_uploaded"]:
    st.warning("🚫 You've already uploaded images in this session. Upload not allowed again.")
else:
    if zip_file is not None:
        if st.button("Upload Images"):
            total_images = 0
            successful_uploads = 0
            failed_files = []

            with zipfile.ZipFile(zip_file, "r") as archive:
                # Count valid images
                image_files = [
                    f for f in archive.infolist()
                    if f.filename.lower().endswith((".jpg", ".jpeg", ".png"))
                ]
                total_images = len(image_files)

                if total_images != required_images:
                    st.error(f"❌ You uploaded {total_images} image(s), but exactly {required_images} are required.")
                    st.stop()

                # Upload images
                for file_info in image_files:
                    with archive.open(file_info.filename) as file_data:
                        files = {
                            "image": (file_info.filename, file_data, "image/jpeg")
                        }
                        data = {
                            "batch_id": batch_id
                        }
                        res = requests.post(API_URL, files=files, data=data)
                        if res.status_code == 200:
                            st.success(f"✅ uploaded {file_info.filename}")
                            successful_uploads += 1
                        else:
                            failed_files.append(file_info.filename)
                            st.error(f"❌ Failed to upload {file_info.filename}")

            # Final result
            if successful_uploads == total_images:
                st.success(f"🎉 All {successful_uploads} images uploaded from {zip_file.name}")
                st.session_state["has_uploaded"] = True
            else:
                st.error(f"⚠️ Only {successful_uploads}/{total_images} images uploaded successfully.")
                if failed_files:
                    st.warning("❌ Failed files: " + ", ".join(failed_files))
