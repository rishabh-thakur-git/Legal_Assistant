import os
import re
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from ml_engine import calculate_severity
from prompts import (
    full_case_analysis_prompt,
    lawyer_guilty_verdict_prompt,
    lawyer_not_guilty_verdict_prompt
)


# ENV & GROQ SETUP

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Andha Kanoon, an AI legal assistant. "
                    "This interaction is strictly for educational and legal analysis purposes. "
                    "Do not provide instructions for illegal activities. "
                    "Only explain legal provisions, procedures, and consequences under Indian law."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content



# INPUT VALIDATION

def valid_story(text: str) -> bool:
    return len(text.strip()) >= 30 and bool(re.search(r"[A-Za-z]", text))



# PAGE CONFIG

st.set_page_config(
    page_title="Andha Kanoon ⚖️",
    page_icon="⚖️",
    layout="wide"
)


# BASIC CLEAN UI CSS

st.markdown("""
<style>
.block {
    background-color: #0f172a;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)


# SESSION STATE

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "memory" not in st.session_state:
    st.session_state.memory = []


# SIDEBAR

with st.sidebar:
    st.markdown("## ⚖️ ANDHA KANOON")
    st.caption("Your Indian Legal Assistant")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["Case Input", "Analysis", "Verdict", "Memory"]
    )
    st.markdown("---")


# HEADER

st.markdown(
    "<h1 style='text-align:center;'>⚖️ ANDHA KANOON</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:#9ca3af;'>Aapki Seva Mein</p>",
    unsafe_allow_html=True
)

st.divider()


# CASE INPUT

if page == "Case Input":
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("📝 Case Details")

    story = st.text_area("Case Description", height=180)
    truth = st.slider("Truth Percentage (%)", 0, 100, 50)
    case_type = st.selectbox(
        "Case Type",
        ["Select", "Theft", "Violence", "Cyber Crime", "Harassment", "Murder", "Other"]
    )

    uploaded = st.file_uploader("Upload Evidence (optional)", ["jpg", "png", "mp4"])

    evidence_type = "No Evidence"
    if uploaded:
        if uploaded.type.startswith("image"):
            evidence_type = "Image Evidence"
            st.image(uploaded)
        else:
            evidence_type = "Video Evidence"
            st.video(uploaded)

    evidence_desc = st.text_area("Evidence Description")
    additional = st.text_area("Additional Statement")

    if st.button("Analyze Case"):
        if not valid_story(story):
            st.error("Please enter a meaningful case description (minimum 30 characters).")
        elif case_type == "Select":
            st.error("Please select a valid case type.")
        else:
            severity = calculate_severity(story, truth, case_type)

            prompt = full_case_analysis_prompt(
                story,
                additional or "None",
                truth,
                severity,
                case_type,
                evidence_type,
                evidence_desc or "Not provided"
            )

            with st.spinner("Analyzing under Indian Law..."):
                analysis = get_ai_response(prompt)

            st.session_state.analysis_done = True
            st.session_state.analysis = analysis
            st.session_state.severity = severity
            st.session_state.story = story
            st.session_state.case_type = case_type
            st.session_state.evidence_type = evidence_type
            st.session_state.memory.append((case_type, severity, story, analysis))

            st.success("Case analysis completed.")
    st.markdown("</div>", unsafe_allow_html=True)


# ANALYSIS

if page == "Analysis" and st.session_state.analysis_done:
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("📊 Legal Analysis")

    sev = st.session_state.severity
    st.write(f"**Severity Score:** {sev}/100")
    st.progress(sev / 100)

    st.write(st.session_state.analysis)
    st.markdown("</div>", unsafe_allow_html=True)


# VERDICT

if page == "Verdict" and st.session_state.analysis_done:
    st.markdown("<div class='block'>", unsafe_allow_html=True)
    st.subheader("⚖️ Legal Opinion")

    verdict = st.radio("Your Position", ["Guilty", "Not Guilty"], horizontal=True)

    summary = f"""
Case Type: {st.session_state.case_type}
Severity: {st.session_state.severity}/100
Evidence: {st.session_state.evidence_type}

Story:
{st.session_state.story}
"""

    if verdict == "Guilty":
        response = get_ai_response(lawyer_guilty_verdict_prompt(summary))
    else:
        response = get_ai_response(lawyer_not_guilty_verdict_prompt(summary))

    st.write(response)
    st.markdown("</div>", unsafe_allow_html=True)


# MEMORY

if page == "Memory":
    st.subheader("🧠 Case Memory")

    if not st.session_state.memory:
        st.info("No previous cases.")
    else:
        for i, m in enumerate(st.session_state.memory, 1):
            with st.expander(f"Case {i} • {m[0]} • Severity {m[1]}/100"):
                st.write("Case Story:")
                st.write(m[2])
                st.write("Legal Analysis:")
                st.write(m[3])
