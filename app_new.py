import streamlit as st
import json
from anthropic import Anthropic

# Initialize Anthropic client
client = Anthropic()

# Set page config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
)

# Title
st.markdown("# 📄 AI Resume Analyzer")
st.markdown("Get instant AI-powered analysis of your resume")

# Sidebar
with st.sidebar:
    st.header("Instructions")
    st.info("""
    **How to use:**
    1. Paste your resume text
    2. Enter target role (optional)
    3. Click "Analyze Resume"
    4. Get instant AI analysis
    """)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Paste Your Resume")
    resume_text = st.text_area(
        "Enter resume content here",
        height=300,
        placeholder="Copy and paste your resume text here..."
    )

with col2:
    st.subheader("⚙️ Settings")
    job_role = st.text_input(
        "Target Job Role (Optional)",
        placeholder="e.g., Data Scientist, Software Engineer",
    )
    industry = st.selectbox(
        "Industry Focus (Optional)",
        ["General", "Technology", "Finance", "Healthcare", "Marketing", "Sales", "Management"]
    )

# Function to analyze resume with Claude
def analyze_resume(resume_text, job_role, industry):
    """Send resume to Claude for analysis"""
    
    prompt = f"""You are an expert HR consultant and resume reviewer. Analyze the following resume and provide a comprehensive evaluation.

RESUME TEXT:
{resume_text}

TARGET JOB ROLE: {job_role if job_role else 'Any position'}
INDUSTRY: {industry}

Please provide your analysis in the following EXACT JSON format:

{{
    "resume_score": <number 0-8>,
    "score_explanation": "<brief explanation of the score>",
    "red_flags": [
        "<red flag 1>",
        "<red flag 2>",
        "<red flag 3>"
    ],
    "improvements": [
        {{
            "area": "<specific section>",
            "current": "<what's currently there>",
            "suggestion": "<improvement suggestion>",
            "priority": "<High/Medium/Low>"
        }},
        {{
            "area": "<specific section>",
            "current": "<what's currently there>",
            "suggestion": "<improvement suggestion>",
            "priority": "<High/Medium/Low>"
        }}
    ],
    "career_opportunities": [
        {{
            "role": "<job title>",
            "why_suited": "<why this resume fits>",
            "potential_salary_range": "<estimated range>"
        }},
        {{
            "role": "<job title>",
            "why_suited": "<why this resume fits>",
            "potential_salary_range": "<estimated range>"
        }}
    ],
    "key_strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
    "overall_feedback": "<2-3 sentence summary>"
}}

IMPORTANT: Return ONLY valid JSON, no other text or markdown."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        analysis = json.loads(response_text)
        return analysis
    
    except json.JSONDecodeError:
        st.error("Error parsing AI response. Please try again.")
        return None
    except Exception as e:
        st.error(f"Error analyzing resume: {str(e)}")
        return None

# Analyze button
if st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
    if not resume_text.strip():
        st.error("Please enter your resume text first!")
    else:
        with st.spinner("Analyzing your resume with AI..."):
            analysis = analyze_resume(resume_text, job_role, industry)
            
            if analysis:
                # Display Results
                st.markdown("---")
                st.markdown("## 📊 Analysis Results")
                
                # Score Card
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    score = analysis.get("resume_score", 0)
                    st.metric("Resume Score", f"{score}/8")
                
                with col2:
                    num_improvements = len(analysis.get("improvements", []))
                    st.metric("Improvements", num_improvements)
                
                with col3:
                    num_opportunities = len(analysis.get("career_opportunities", []))
                    st.metric("Opportunities", num_opportunities)
                
                # Score Explanation
                st.info(f"**Score Explanation:** {analysis.get('score_explanation', 'N/A')}")
                
                # Key Strengths
                st.markdown("### ✨ Key Strengths")
                strengths = analysis.get("key_strengths", [])
                for strength in strengths:
                    st.success(f"✓ {strength}")
                
                # Red Flags
                st.markdown("### 🚩 Red Flags Detected")
                red_flags = analysis.get("red_flags", [])
                if red_flags:
                    for flag in red_flags:
                        st.warning(f"⚠️ {flag}")
                else:
                    st.success("No major red flags detected!")
                
                # Improvements
                st.markdown("### 💡 Recommended Improvements")
                improvements = analysis.get("improvements", [])
                if improvements:
                    for imp in improvements:
                        priority = imp.get("priority", "Medium")
                        icon = "🔴" if priority == "High" else "🟡" if priority == "Medium" else "🟢"
                        with st.expander(f"{icon} {imp.get('area', 'Improvement')} ({priority})"):
                            st.write(f"**Current:** {imp.get('current', 'N/A')}")
                            st.write(f"**Suggestion:** {imp.get('suggestion', 'N/A')}")
                
                # Career Opportunities
                st.markdown("### 🎯 Career Opportunities")
                opportunities = analysis.get("career_opportunities", [])
                if opportunities:
                    for opp in opportunities:
                        st.info(f"**{opp.get('role', 'N/A')}**\n\n{opp.get('why_suited', 'N/A')}\n\n**Salary:** {opp.get('potential_salary_range', 'N/A')}")
                
                # Overall Feedback
                st.markdown("### 📝 Overall Assessment")
                st.success(analysis.get("overall_feedback", "N/A"))

st.markdown("---")
st.caption("AI Resume Analyzer | Powered by Claude AI")
