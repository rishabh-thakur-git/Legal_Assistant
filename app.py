import os
import re
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from ml_engine import calculate_severity
from prompts import full_case_analysis_prompt


# ENV + GROQ SETUP

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_response(prompt: str) -> str:
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are Andha Kanoon, an Indian legal assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return completion.choices[0].message.content



# BASIC INPUT VALIDATION

def is_valid_story(text: str) -> bool:
    if len(text.strip()) < 30:
        return False
    if not re.search(r"[a-zA-Z]", text):
        return False
    return True



# STREAMLIT CONFIG

st.set_page_config(
    page_title="Andha Kanoon ⚖️",
    page_icon="⚖️",
    layout="wide"
)


# SESSION STATE (MEMORY)

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "memory" not in st.session_state:
    st.session_state.memory = []  # stores past cases



# HEADER

st.title("⚖️ Andha Kanoon")
st.caption("AI + ML based Indian Legal Assistant (Powered by Groq) 🇮🇳")

st.info(
    "⚠️ Please provide a meaningful and complete case description for analysis."
)

st.divider()


# CASE DETAILS

st.subheader("📖 Case Details")

story = st.text_area(
    "Describe the case",
    placeholder="Explain what happened, where it happened, who was involved, and how..."
)

truth_percent = st.slider("Truth Percentage (%)", 0, 100, 50)

case_type = st.selectbox(
    "Case Type",
    ["Select", "Theft", "Violence", "Cyber Crime", "Harassment", "Murder", "Other"]
)


# EVIDENCE

st.subheader("📁 Evidence Submission")

uploaded_file = st.file_uploader(
    "Upload evidence (photo or video)",
    type=["jpg", "jpeg", "png", "mp4"]
)

evidence_type = "No Evidence"
if uploaded_file:
    if uploaded_file.type.startswith("image"):
        evidence_type = "Image Evidence"
        st.image(uploaded_file, use_column_width=True)
    else:
        evidence_type = "Video Evidence"
        st.video(uploaded_file)

evidence_description = st.text_area(
    "Describe what the evidence shows",
    placeholder="Example: CCTV footage shows the accused entering the shop at night..."
)


# ADDITIONAL STATEMENT

st.subheader("🗣️ Additional Statement (Optional)")

additional_statement = st.text_area(
    "Any additional explanation or clarification?"
)


# ANALYZE CASE

if st.button("🧠 Analyze Case"):
    if not is_valid_story(story):
        st.error("❌ Please enter a valid and meaningful case statement (at least 30 characters).")

    elif case_type == "Select":
        st.error("❌ Please select a valid case type.")

    else:
        severity = calculate_severity(
            story=story,
            truth=truth_percent,
            case_type=case_type
        )

        prompt = full_case_analysis_prompt(
            story=story,
            additional_statement=additional_statement or "No additional statement provided",
            truth=truth_percent,
            severity=severity,
            case_type=case_type,
            evidence_type=evidence_type,
            evidence_description=evidence_description or "Not provided"
        )

        with st.spinner("Analyzing under Indian Law..."):
            analysis = get_ai_response(prompt)

        # Save to memory
        st.session_state.memory.append({
            "Story": story,
            "Case Type": case_type,
            "Severity": severity,
            "Analysis": analysis
        })

        st.session_state.analysis_done = True
        st.session_state.severity = severity
        st.session_state.analysis = analysis

        st.subheader("📊 Severity Score")
        st.progress(severity / 100)
        st.write(f"Severity: **{severity}/100**")

        st.subheader("📜 Legal Analysis")
        st.write(analysis)


# VERDICT (RULE-BASED)

if st.session_state.analysis_done:
    st.divider()
    st.subheader("⚖️ Verdict")

    verdict = st.radio(
        "Based on the above analysis, are you:",
        ["Select", "Guilty", "Not Guilty"],
        horizontal=True
    )

    if verdict == "Guilty":
        st.subheader("🚨 Legal Consequences")
        if st.session_state.severity >= 70:
            st.write("Serious offence. Arrest, charges, and imprisonment possible.")
        else:
            st.write("Minor/moderate offence. Fine, warning, or settlement possible.")

    elif verdict == "Not Guilty":
        st.subheader("🛡️ Legal Rights & Procedure")
        st.write("""
- FIR registration and investigation  
- Right to a lawyer  
- Presumption of innocence  
- Trial before competent court
""")


# MEMORY SECTION

st.divider()
st.subheader("🧠 Case Memory")

if not st.session_state.memory:
    st.write("No cases analyzed yet.")
else:
    for i, case in enumerate(st.session_state.memory, start=1):
        with st.expander(f"Case {i} – {case['Case Type']}"):
            st.write(f"**Severity:** {case['Severity']}/100")
            st.write("**Story:**")
            st.write(case["Story"])
            st.write("**Legal Analysis:**")
            st.write(case["Analysis"])
