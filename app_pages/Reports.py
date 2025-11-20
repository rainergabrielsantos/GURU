from fpdf import FPDF
import streamlit as st
from io import BytesIO

st.title("📄 Welcome to Reports!")

def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This is a dynamically generated sample report!", ln=True, align='C')

    # fpdf2 ≥ 2.7 returns bytearray already
    pdf_bytes = pdf.output(dest="S")
    return BytesIO(pdf_bytes)

if st.button("Generate PDF Report"):
    pdf_data = create_pdf()
    st.download_button(
        label="⬇️ Download PDF",
        data=pdf_data,
        file_name="Sample_Report.pdf",
        mime="application/pdf"
    )
    st.success("✅ Report has been created! Click above to download.")
