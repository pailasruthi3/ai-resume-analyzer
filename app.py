import streamlit as st
import pypdf
import os
from anthropic import Anthropic

# Initialize Anthropic client
client = Anthropic()

# Set page config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        color: #1f77e4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .section-header {
        color: #1f77e4;
        font-size: 1.3em;
        font-weight: bold;
        margin-top: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #1f77e4;
    }
    .score-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 2em;
        font-weight: bold;
    }
    .red-flag {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 10px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .improvement {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 10px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .opportunity {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 10px;
        margin: 10px 0;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Description
st.markdown('<div class="main-header">📄 AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown("Get instant AI-powered analysis of your resume with scoring, red flags, improvements, and career opportunities.")

# Sidebar
with st.sidebar:
    st.header("Instructions")
    st.info("""
    **How to use:**
    1. Upload your resume (PDF format)
    2. Click "Analyze Resume"
    3. Get instant AI analysis
    
    **What you'll get:**
    - Resume Score (0-8)
    - Red Flags Detection
    - Specific Improvements
    - Career Opportunities
    """)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload your resume in PDF format"
    )

with col2:
    st.subheader("⚙️ Settings")
    job_role = st.text_input(
        "Target Job Role (Optional)",
        placeholder="e.g., Data Scientist, Software Engineer, Product Manager",
        help="Specify your target role for more relevant feedback"
    )
    industry = st.selectbox(
        "Industry Focus (Optional)",
        ["General", "Technology", "Finance", "Healthcare", "Marketing", "Sales", "Management"]
    )

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

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
            "area": "<specific section/line>",
            "current": "<what's currently there>",
            "suggestion": "<detailed improvement suggestion>",
            "priority": "<High/Medium/Low>"
        }},
        {{
            "area": "<specific section/line>",
            "current": "<what's currently there>",
            "suggestion": "<detailed improvement suggestion>",
            "priority": "<High/Medium/Low>"
        }}
    ],
    "career_opportunities": [
        {{
            "role": "<job title>",
            "why_suited": "<why this resume fits this role>",
            "potential_salary_range": "<estimated range>"
        }},
        {{
            "role": "<job title>",
            "why_suited": "<why this resume fits this role>",
            "potential_salary_range": "<estimated range>"
        }}
    ],
    "key_strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
    "overall_feedback": "<2-3 sentence summary of overall assessment>"
}}

IMPORTANT: Return ONLY valid JSON, no other text or markdown. Make sure the JSON is properly formatted and can be parsed."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract and parse the response
        response_text = message.content[0].text
        
        # Try to parse JSON
        import json
        analysis = json.loads(response_text)
        return analysis
    
    except json.JSONDecodeError:
        st.error("Error parsing AI response. Please try again.")
        return None
    except Exception as e:
        st.error(f"Error analyzing resume: {str(e)}")
        return None

# Analyze button and results
if uploaded_file is not None:
    st.markdown("---")
    
    if st.button("🔍 Analyze Resume", use_container_width=True, type="primary"):
        with st.spinner("Analyzing your resume with AI... This may take a moment."):
            # Extract text from PDF
            resume_text = extract_text_from_pdf(uploaded_file)
            
            if resume_text:
                # Analyze with Claude
                analysis = analyze_resume(resume_text, job_role, industry)
                
                if analysis:
                    # Display Results
                    st.markdown('<div class="section-header">📊 Analysis Results</div>', unsafe_allow_html=True)
                    
                    # Score Card
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        score = analysis.get("resume_score", 0)
                        st.markdown(f'<div class="score-box">{score}/8</div>', unsafe_allow_html=True)
                        st.markdown("<center><b>Resume Score</b></center>", unsafe_allow_html=True)
                    
                    with col2:
                        num_improvements = len(analysis.get("improvements", []))
                        st.metric("Improvements Needed", num_improvements)
                    
                    with col3:
                        num_opportunities = len(analysis.get("career_opportunities", []))
                        st.metric("Opportunities", num_opportunities)
                    
                    # Score Explanation
                    st.info(f"**Score Explanation:** {analysis.get('score_explanation', 'N/A')}")
                    
                    # Key Strengths
                    st.markdown('<div class="section-header">✨ Key Strengths</div>', unsafe_allow_html=True)
                    strengths = analysis.get("key_strengths", [])
                    for strength in strengths:
                        st.success(f"✓ {strength}")
                    
                    # Red Flags
                    st.markdown('<div class="section-header">🚩 Red Flags Detected</div>', unsafe_allow_html=True)
                    red_flags = analysis.get("red_flags", [])
                    if red_flags:
                        for flag in red_flags:
                            st.markdown(f'<div class="red-flag">⚠️ {flag}</div>', unsafe_allow_html=True)
                    else:
                        st.success("No major red flags detected!")
                    
                    # Improvements
                    st.markdown('<div class="section-header">💡 Recommended Improvements</div>', unsafe_allow_html=True)
                    improvements = analysis.get("improvements", [])
                    if improvements:
                        for i, imp in enumerate(improvements, 1):
                            priority_color = "🔴" if imp.get("priority") == "High" else "🟡" if imp.get("priority") == "Medium" else "🟢"
                            with st.expander(f"{priority_color} {imp.get('area', 'Improvement')} - {imp.get('priority', 'Medium')} Priority"):
                                st.markdown(f"**Current:** {imp.get('current', 'N/A')}")
                                st.markdown(f"**Suggestion:** {imp.get('suggestion', 'N/A')}")
                    
                    # Career Opportunities
                    st.markdown('<div class="section-header">🎯 Career Opportunities</div>', unsafe_allow_html=True)
                    opportunities = analysis.get("career_opportunities", [])
                    if opportunities:
                        for opp in opportunities:
                            st.markdown(f'<div class="opportunity"><b>{opp.get("role", "N/A")}</b><br>{opp.get("why_suited", "N/A")}<br><b>Potential Salary:</b> {opp.get("potential_salary_range", "N/A")}</div>', unsafe_allow_html=True)
                    
                    # Overall Feedback
                    st.markdown('<div class="section-header">📝 Overall Assessment</div>', unsafe_allow_html=True)
                    st.info(analysis.get("overall_feedback", "N/A"))
                    
                    # Download Summary
                    st.markdown("---")
                    if st.button("📥 Download Analysis as Text"):
                        summary = f"""
RESUME ANALYSIS SUMMARY
{'='*50}

Score: {analysis.get('resume_score')}/8
{analysis.get('score_explanation')}

KEY STRENGTHS:
{chr(10).join([f'✓ {s}' for s in analysis.get('key_strengths', [])])}

RED FLAGS:
{chr(10).join([f'⚠️ {f}' for f in analysis.get('red_flags', [])])}

IMPROVEMENTS:
{chr(10).join([f"• {i.get('area')}: {i.get('suggestion')}" for i in analysis.get('improvements', [])])}

CAREER OPPORTUNITIES:
{chr(10).join([f"• {o.get('role')} - {o.get('why_suited')}" for o in analysis.get('career_opportunities', [])])}
"""
                        st.download_button("Download Summary", summary, "resume_analysis.txt")
else:
    st.warning("👆 Please upload a resume (PDF format) to get started!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
<p><small>AI Resume Analyzer | Powered by Claude AI | Built with Streamlit</small></p>
</div>
""", unsafe_allow_html=True)
