import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="Roofing Scope Calculator", layout="centered")

st.title("📄 Roofing Scope Line Item Calculator")

uploaded_file = st.file_uploader("Upload Insurance Scope PDF", type="pdf")

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    # Extract line items with quantity, unit, and RCV
    line_pattern = r"(\d+\.\d{2})\s+(EA|LF|SQ|SF|SY)\s+\—\s+\$(\d{1,6}\.\d{2})"
    matches = re.findall(line_pattern, text)

    if not matches:
        st.warning("No line items found in PDF.")
    else:
        st.subheader("Select Completed Line Items")

        line_items = []
        for qty, unit, price in matches:
            label = f"{qty} {unit} — ${price}"
            rcv = float(price)
            line_items.append((label, rcv))

        total = 0
        for i, (label, rcv) in enumerate(line_items):
            checkbox_key = f"line_{i}_{hash(label)}"
            if st.checkbox(label, key=checkbox_key):
                total += rcv

        st.markdown("---")
        st.metric("Total RCV of Selected Items", f"${total:,.2f}")
