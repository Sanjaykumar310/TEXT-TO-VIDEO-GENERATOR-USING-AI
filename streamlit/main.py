import requests
import streamlit as st
import uuid

st.set_page_config(page_title="Text to Video", layout="wide")
st.title("📽️ Welcome to the Text-to-Video Project")

# 🔁 Cleanup inactive batches older than 1 hour
try:
    API_BASE = st.secrets["api_base"]
    response = requests.post(f"{API_BASE}/cleanup-inactive-batches/")
    if response.status_code == 200:
        result = response.json()
        st.info(f"🧹 Cleaned up {result['count']} inactive batch(es).")
    else:
        st.success("✅ No inactive batches found. Everything's clean!")
except Exception as e:
    st.error(f"Cleanup error: {e}")

# Assign a new batch_id for this visitor
if "batch_id" not in st.session_state:
    st.session_state["batch_id"] = str(uuid.uuid4())

