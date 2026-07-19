import streamlit as st
import json
import os
import requests

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")

if not api_key:
    st.error("API Key not found")
    st.stop()

st.title("📄 AI Resume Analyzer")
st.write("Paste your resume and get instant AI analysis")

with st.sidebar:
    st.header("How to Use")
    st.info("1. Paste resume text\n2. Add target role (optional)\n3. Click Analyze")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Resume Text")
    resume_text = st.text_area("Paste your resume:", height=300)

with col2:
    st.subheader("Settings")
    job_role = st.text_input("Target Role (optional)")
    industry = st.selectbox("Industry", ["General", "Technology", "Finance", "Healthcare", "Marketing", "Sales"])

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
            response_text = result["content"][0]["text"]
            return json.loads(response_text)
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
    if not resume_text.strip():
        st.error("Enter resume text!")
    else:
        with st.spinner("Analyzing..."):
            result = analyze_resume(resume_text, job_role, industry)
            
            if result:
                st.markdown("---")
                st.header("Results")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Score", f"{result.get('resume_score', 0)}/8")
                col2.metric("Improvements", len(result.get("improvements", [])))
                col3.metric("Opportunities", len(result.get("career_opportunities", [])))
                
                st.info(f"**{result.get('score_explanation', '')}**")
                
                st.subheader("✨ Strengths")
                for s in result.get("key_strengths", []):
                    st.success(f"✓ {s}")
                
                st.subheader("🚩 Red Flags")
                flags = result.get("red_flags", [])
                if flags:
                    for f in flags:
                        st.warning(f"⚠️ {f}")
                else:
                    st.success("No red flags!")
                
                st.subheader("💡 Improvements")
                for imp in result.get("improvements", []):
                    icon = "🔴" if imp.get("priority") == "High" else "🟡" if imp.get("priority") == "Medium" else "🟢"
                    with st.expander(f"{icon} {imp.get('area')}"):
                        st.write(f"Current: {imp.get('current')}")
                        st.write(f"Suggestion: {imp.get('suggestion')}")
                
                st.subheader("🎯 Opportunities")
                for opp in result.get("career_opportunities", []):
                    st.info(f"**{opp.get('role')}**\n\n{opp.get('why_suited')}\n\nSalary: {opp.get('potential_salary_range')}")
                
                st.subheader("📝 Assessment")
                st.success(result.get("overall_feedback", ""))

st.divider()
st.caption("AI Resume Analyzer | Powered by Claude")
