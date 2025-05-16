import streamlit as st
import requests

st.set_page_config(page_title="Complete", layout="wide")
st.title("✅ Final Step: Clean Up Session Data")

batch_id = st.session_state.get("batch_id")

if not batch_id:
    st.warning("No batch ID found. Nothing to delete.")
else:
    if st.button("Finished"):
        DELETE_URL = f"http://127.0.0.1:8000/api/delete-batch/{batch_id}/"
        try:
            res = requests.delete(DELETE_URL)
            if res.status_code == 200:
                st.success(f"Batch {batch_id} and its data deleted.")
                del st.session_state["batch_id"]
            else:
                st.error(f"Failed to delete batch. Status code: {res.status_code}")
        except Exception as e:
            st.error(f"API error: {e}")
