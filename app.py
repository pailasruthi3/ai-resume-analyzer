import streamlit as st
import json
import os
from anthropic import Anthropic

# DEBUG: Check what we're getting
try:
    api_key_from_secrets = st.secrets.get("ANTHROPIC_API_KEY")
except Exception as e:
    api_key_from_secrets = None

api_key_from_env = os.environ.get("ANTHROPIC_API_KEY")

# Show debug info
st.write("🔍 DEBUG INFO:")
st.write(f"Key from secrets: {'Found' if api_key_from_secrets else 'NOT FOUND'}")
st.write(f"Key from env: {'Found' if api_key_from_env else 'NOT FOUND'}")

api_key = api_key_from_secrets or api_key_from_env

if not api_key:
    st.error("API KEY NOT FOUND")
    st.warning("Add ANTHROPIC_API_KEY to Streamlit Cloud Secrets")
    st.stop()

st.success("API Key found!")

try:
    client = Anthropic(api_key=api_key)
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.stop()

st.title("📄 AI Resume Analyzer")
