
import streamlit as st
import pdfplumber
import re

st.title("Roofing Scope Calculator from Insurance PDF")

uploaded_file = st.file_uploader("Upload Insurance Scope (PDF)", type=["pdf"])

line_items = []
total = 0

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            lines = text.split('\n')
            for line in lines:
                # Simple match for scope-style lines (e.g., quantity + unit + RCV)
                match = re.search(r"(\d+\.\d+)(SQ|LF|EA)\s+[\d.]+\s+[\d.]+\s+([\d,]+\.\d+)", line)
                if match:
                    qty = match.group(1)
                    unit = match.group(2)
                    rcv = float(match.group(3).replace(',', ''))
                    label = f"{qty} {unit} — ${rcv:,.2f}"
                    line_items.append((label, rcv))

    st.subheader("Select Completed Line Items")
    for label, rcv in line_items:
        if st.checkbox(label):
            total += rcv

    st.markdown(f"### Total Selected RCV: **${total:,.2f}**")
else:
    st.info("Upload a PDF to begin.")
