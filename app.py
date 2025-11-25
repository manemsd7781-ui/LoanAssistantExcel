# app.py
import streamlit as st
import ui_capture

# --- MAIN APP LAYOUT ---
st.set_page_config(page_title="BDO Loan Eligibility Assistant", layout="wide")
st.title("💬 BDO Loan Eligibility Assistant")
st.caption("Capture lead details and get instant eligibility results.")

# Always show the Lead Capture view (Admin removed)
ui_capture.display_lead_capture()
