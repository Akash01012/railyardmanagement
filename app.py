import streamlit as st
import subprocess

st.set_page_config(page_title="🚆 RailYard Protocol Simulation", layout="wide")
st.title("🚆 RailYard Protocol Simulation")

st.write("Press the button below to run the RailYard simulation:")

# Button to run simulation
if st.button("Run Simulation"):
    st.write("Running protocol...")

    # Use subprocess to run main_file.py and capture output line by line
    process = subprocess.Popen(
        ["python", "main_file.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Stream output to Streamlit in real-time
    output_placeholder = st.empty()
    full_output = ""
    for line in process.stdout:
        full_output += line
        output_placeholder.text(full_output)
    
    process.wait()
    st.success("Simulation Finished ✅")
