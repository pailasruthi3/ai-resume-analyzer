import streamlit as st
import json
import os
import requests
import pypdf

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide", initial_sidebar_state="collapsed")

# Professional CSS
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    body {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .main {
        background-color: #ffffff;
    }
    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1rem;
        font-weight: 600;
    }
    
    h1 {
        color: #1e3a8a;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    h2 {
        color: #1e3a8a;
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 1.5rem;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
    }
    
    h3 {
        color: #1e3a8a;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .stFileUploader {
        border: 2px dashed #3b82f6;
        border-radius: 12px;
        padding: 20px;
        background-color: #f0f9ff;
    }
    
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        font-family: 'Courier New', monospace;
    }
    
    .stTextInput input {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
    }
    
    .stSelectbox select {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .score-display {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .score-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .strength-card {
        background-color: #ecfdf5;
        border-left: 5px solid #10b981;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-weight: 500;
    }
    
    .flag-card {
        background-color: #fef2f2;
        border-left: 5px solid #ef4444;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-weight: 500;
    }
    
    .improvement-card {
        background-color: #fffbeb;
        border-left: 5px solid #f59e0b;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .opportunity-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        padding: 12px 32px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid #e2e8f0;
    }
    
    .header-section {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
        padding: 40px 20px;
        border-radius: 12px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.2);
    }
    
    .header-section h1 {
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .header-section p {
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    .expander {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    [data-testid="stExpander"] {
        border-radius: 8px;
    }
    
    .stInfo {
        background-color: #dbeafe;
        border-left: 5px solid #3b82f6;
        border-radius: 8px;
    }
    
    .stSuccess {
        background-color: #dcfce7;
        border-left: 5px solid #10b981;
        border-radius: 8px;
    }
    
    .stWarning {
        background-color: #fef3c7;
        border-left: 5px solid #f59e0b;
        border-radius: 8px;
    }
    
    .stError {
        background-color: #fee2e2;
        border-left: 5px solid #ef4444;
        border-radius: 8px;
    }
    
    .input-section {
        background-color: #f8fafc;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 25px;
    }
    
    .result-section {
        background-color: #f8fafc;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-top: 25px;
    }
    
    .divider {
        margin: 2rem 0;
        border-top: 2px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    st.error("❌ API Key not found. Add ANTHROPIC_API_KEY to Streamlit Secrets.")
    st.stop()

# Header
st.markdown("""
<div class="header-section">
    <h1>📄 AI Resume Analyzer</h1>
    <p>Professional Resume Analysis Powered by Claude AI</p>
</div>
""", unsafe_allow_html=True)

# Input Section
st.markdown('<div class="input-section">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📤 Upload PDF Resume")
    uploaded_file = st.file_uploader("Choose your resume PDF", type="pdf", label_visibility="collapsed")
    
    resume_text = ""
    if uploaded_file:
        try:
            pdf_reader = pypdf.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                resume_text += page.extract_text()
            st.success(f"✅ PDF loaded successfully ({len(resume_text)} characters)")
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")

with col2:
    st.markdown("### 📝 Or Paste Resume Text")
    pasted_text = st.text_area("Paste your resume content:", height=200, label_visibility="collapsed", placeholder="Paste your resume here...")
    if pasted_text:
        resume_text = pasted_text

# Settings
st.markdown("### ⚙️ Analysis Settings")
settings_col1, settings_col2, settings_col3 = st.columns([1, 1, 1])

with settings_col1:
    job_role = st.text_input("Target Job Role (optional)", placeholder="e.g., Data Scientist")

with settings_col2:
    industry = st.selectbox("Industry Focus", ["General", "Technology", "Finance", "Healthcare", "Marketing", "Sales", "Management"])

with settings_col3:
    st.write("")  # Spacing

st.markdown('</div>', unsafe_allow_html=True)

def analyze_resume(text, role, ind):
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    
    prompt = f"""Analyze this resume and return ONLY valid JSON:

RESUME: {text}
ROLE: {role or 'Any'}
INDUSTRY: {ind}

Return ONLY this JSON (no other text):
{{
    "resume_score": <0-8>,
    "score_explanation": "<brief>",
    "red_flags": ["<flag1>", "<flag2>", "<flag3>"],
    "improvements": [
        {{"area": "<area>", "current": "<current>", "suggestion": "<suggestion>", "priority": "<High/Medium/Low>"}},
        {{"area": "<area>", "current": "<current>", "suggestion": "<suggestion>", "priority": "<High/Medium/Low>"}}
    ],
    "career_opportunities": [
        {{"role": "<role>", "why_suited": "<why>", "potential_salary_range": "<range>"}},
        {{"role": "<role>", "why_suited": "<why>", "potential_salary_range": "<range>"}}
    ],
    "key_strengths": ["<s1>", "<s2>", "<s3>"],
    "overall_feedback": "<summary>"
}}"""

    data = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        if "content" in result and len(result["content"]) > 0:
            response_text = result["content"][0].text
            return json.loads(response_text)
        return None
    except Exception as e:
        st.error(f"Analysis Error: {str(e)}")
        return None

# Analyze Button
col_button_space = st.columns([1, 1, 1])
with col_button_space[1]:
    analyze_clicked = st.button("🔍 Analyze My Resume", use_container_width=True)

if analyze_clicked:
    if not resume_text.strip():
        st.error("⚠️ Please upload a PDF or paste resume text to analyze!")
    else:
        progress_bar = st.progress(0)
        with st.spinner("🤖 Analyzing your resume with AI..."):
            result = analyze_resume(resume_text, job_role, industry)
            progress_bar.progress(100)
            
            if result:
                # Results Section
                st.markdown('<div class="result-section">', unsafe_allow_html=True)
                
                st.markdown("## 📊 Analysis Results")
                
                # Score Metrics
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                with metric_col1:
                    score = result.get('resume_score', 0)
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="score-label">Resume Score</div>
                        <div class="score-display">{score}/8</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric_col2:
                    improvements_count = len(result.get("improvements", []))
                    st.metric("Areas to Improve", improvements_count)
                
                with metric_col3:
                    opportunities_count = len(result.get("career_opportunities", []))
                    st.metric("Career Paths", opportunities_count)
                
                # Score Explanation
                st.info(f"**📌 Analysis Summary:** {result.get('score_explanation', 'N/A')}")
                
                # Strengths Section
                st.markdown("### ✨ Key Strengths")
                for strength in result.get("key_strengths", []):
                    st.markdown(f'<div class="strength-card">✓ {strength}</div>', unsafe_allow_html=True)
                
                # Red Flags Section
                st.markdown("### 🚩 Red Flags Detected")
                red_flags = result.get("red_flags", [])
                if red_flags:
                    for flag in red_flags:
                        st.markdown(f'<div class="flag-card">⚠️ {flag}</div>', unsafe_allow_html=True)
                else:
                    st.success("✅ No major red flags detected!")
                
                # Improvements Section
                st.markdown("### 💡 Recommended Improvements")
                improvements = result.get("improvements", [])
                if improvements:
                    for idx, imp in enumerate(improvements, 1):
                        priority = imp.get("priority", "Medium")
                        icon = "🔴" if priority == "High" else "🟡" if priority == "Medium" else "🟢"
                        
                        with st.expander(f"{icon} {imp.get('area')} ({priority} Priority)", expanded=(idx==1)):
                            col_imp1, col_imp2 = st.columns([1, 1])
                            with col_imp1:
                                st.markdown("**Current:**")
                                st.markdown(f"`{imp.get('current', 'N/A')}`")
                            with col_imp2:
                                st.markdown("**Suggestion:**")
                                st.write(imp.get('suggestion', 'N/A'))
                
                # Career Opportunities Section
                st.markdown("### 🎯 Career Opportunities")
                for opp in result.get("career_opportunities", []):
                    st.markdown(f"""
                    <div class="opportunity-card">
                        <strong>{opp.get('role', 'N/A')}</strong><br><br>
                        {opp.get('why_suited', 'N/A')}<br><br>
                        <strong>💰 Potential Salary Range:</strong> {opp.get('potential_salary_range', 'N/A')}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Overall Assessment Section
                st.markdown("### 📝 Overall Assessment")
                st.success(result.get("overall_feedback", "N/A"))
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Download Summary
                st.divider()
                summary_text = f"""
AI RESUME ANALYSIS REPORT
{'='*60}

SCORE: {result.get('resume_score', 0)}/8
{result.get('score_explanation', '')}

KEY STRENGTHS:
{chr(10).join([f'✓ {s}' for s in result.get('key_strengths', [])])}

RED FLAGS:
{chr(10).join([f'⚠️ {f}' for f in result.get('red_flags', [])])}

IMPROVEMENTS:
{chr(10).join([f"• {i.get('area')}: {i.get('suggestion')}" for i in result.get('improvements', [])])}

CAREER OPPORTUNITIES:
{chr(10).join([f"• {o.get('role')} - {o.get('why_suited')}" for o in result.get('career_opportunities', [])])}

ASSESSMENT:
{result.get('overall_feedback', '')}

{'='*60}
Generated by AI Resume Analyzer
"""
                
                col_download1, col_download2, col_download3 = st.columns([1, 1, 1])
                with col_download2:
                    st.download_button(
                        label="📥 Download Report",
                        data=summary_text,
                        file_name="resume_analysis_report.txt",
                        mime="text/plain"
                    )

# Footer
st.markdown("""
<div class="footer">
    <p>✨ AI Resume Analyzer | Powered by Claude AI | Built with Streamlit ✨</p>
    <p style="font-size: 0.85rem; margin-top: 0.5rem;">Your professional resume companion</p>
</div>
""", unsafe_allow_html=True)
