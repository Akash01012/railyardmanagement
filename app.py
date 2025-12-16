import streamlit as st
import subprocess
import time

st.set_page_config(page_title="RailYard Protocol", layout="centered")
st.title("🚆 RailYard Protocol Simulation")

if st.button("Run Simulation"):
    st.text("Running protocol...\n")

    output_box = st.empty()  # placeholder for live output
    full_output = ""

    process = subprocess.Popen(
        ["python", "main_file.py"],  # <-- your existing CLI script
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    for line in process.stdout:
        full_output += line
        output_box.text(full_output)
        time.sleep(0.05)  # optional: smooth scrolling

    process.stdout.close()
    process.wait()
    st.success("Simulation Finished ✅")
