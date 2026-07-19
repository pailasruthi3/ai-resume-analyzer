import streamlit as st
import json
import os
from anthropic import Anthropic

# Get API key
api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    st.error("API Key not found")
    st.stop()

# Initialize client with compatibility fix
try:
    client = Anthropic(api_key=api_key, timeout=30.0)
except TypeError:
    # Fallback for Python 3.14 compatibility
    client = Anthropic(api_key=api_key)

st.title("📄 AI Resume Analyzer")
