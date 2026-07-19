import streamlit as st
import json
import os
from anthropic import Anthropic

# Get API key from Streamlit secrets or environment
try:
    api_key = st.secrets.get("ANTHROPIC_API_KEY")
except Exception:
    api_key = None

if not api_key:
    api_key = os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    st.error("❌ API Key not found!")
    st.info("Please add ANTHROPIC_API_KEY to Streamlit Cloud Secrets:\n1. Go to Settings\n2. Click 'Secrets'\n3. Add: ANTHROPIC_API_KEY = \"sk-ant-v0-xxxxx...\"")
    st.stop()

# Initialize Anthropic client
try:
    client = Anthropic(api_key=api_key)
except Exception as e:
    st.error(f"Error initializing API: {str(e)}")
    st.stop()

# Set page config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
)

# Title
st.markdown("# 📄 AI Resume Analyzer")
st.markdown("Get instant AI-powered analysis of your
