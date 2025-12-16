import streamlit as st
import subprocess

st.set_page_config(page_title="RailYard Protocol", layout="centered")

st.title("🚆 RailYard Protocol Simulation")

if st.button("Run Simulation"):
    st.text("Running protocol...\n")

    result = subprocess.run(
        ["python", "main_file.py"],
        capture_output=True,
        text=True
    )

    st.text_area(
        "Live Output",
        result.stdout,
        height=400
    )