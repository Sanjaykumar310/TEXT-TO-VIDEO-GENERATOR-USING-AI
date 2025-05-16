import requests
import streamlit as st
import uuid

st.set_page_config(page_title="Text to Video", layout="wide")
st.title("📽️ Welcome to the Text-to-Video Project")

# 🔁 Cleanup inactive batches older than 1 hour
try:
    response = requests.post("http://127.0.0.1:8000/api/cleanup-inactive-batches/")
    if response.status_code == 200:
        result = response.json()
        st.info(f"🧹 Cleaned up {result['count']} inactive batch(es).")
    else:
        st.warning("Cleanup failed.")
except Exception as e:
    st.error(f"Cleanup error: {e}")

# Assign a new batch_id for this visitor
if "batch_id" not in st.session_state:
    st.session_state["batch_id"] = str(uuid.uuid4())





# import streamlit as st
# import requests

# # URL of your Django backend API
# API_URL = "http://127.0.0.1:8000/api/save-script/"  # change this to your deployed URL later

# st.title("📝 Text-to-Video Script Uploader")

# # Input box for script
# script_text = st.text_area("Enter your script here:")

# # Submit button
# if st.button("Submit Script"):
#     if not script_text.strip():
#         st.warning("Please enter some script text.")
#     else:
#         # Prepare data to send
#         payload = {"script": script_text}

#         try:
#             # Send POST request to Django API
#             response = requests.post(API_URL, json=payload)

#             if response.status_code == 200:
#                 data = response.json()
#                 st.success(f"✅ Script saved! ID: {data['id']}")
#             else:
#                 st.error(f"❌ Failed to save script. Status code: {response.status_code}")
#                 st.json(response.json())  # Show error details
#         except Exception as e:
#             st.error(f"🔌 Error connecting to API: {e}")

# import streamlit as st
# import zipfile
# import io
# import requests
# import uuid
# import io
# from PIL import Image

# API_URL = "http://127.0.0.1:8000/api/upload-folder/"
# st.title("📁 Upload a Folder (as .zip)")

# zip_file = st.file_uploader("Upload a .zip file of images", type=["zip"])

# if zip_file is not None:
#     if st.button("Upload Images from Zip"):
#         if "batch_id" not in st.session_state:
#             st.session_state["batch_id"] = str(uuid.uuid4())
#         batch_id = st.session_state["batch_id"]        

#         with zipfile.ZipFile(zip_file, "r") as archive:
#             for file_info in archive.infolist():
#                 if file_info.filename.lower().endswith((".jpg", ".jpeg", ".png")):
#                     with archive.open(file_info.filename) as file_data:
#                         files = {
#                             "image": (file_info.filename, file_data, "image/jpeg")  # You can infer MIME type better
#                         }
#                         data = {
#                             "batch_id": batch_id
#                         }
#                         res = requests.post(API_URL, files=files, data=data)
#                         if res.status_code != 200:
#                             st.error(f"Failed to upload {file_info.filename}")
#         st.success(f"✅ Uploaded all images from {zip_file.name}!")




