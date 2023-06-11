import streamlit as st
from PyPDF2 import PdfReader
from language_tool_python import LanguageTool
from reportlab.pdfgen import canvas
import io

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

def correct_grammar_and_typos(text):
    tool = LanguageTool('en-US')
    matches = tool.check(text)
    corrected_text = tool.correct(text)
    return corrected_text

def save_text_to_pdf(text, output_path):
    packet = io.BytesIO()
    c = canvas.Canvas(packet)
    lines = text.split('\n')
    y = 800
    for line in lines:
        c.drawString(50, y, line)
        y -= 15
    c.save()
    packet.seek(0)
    with open(output_path, 'wb') as file:
        file.write(packet.getvalue())

def main():
    st.title("PDF Grammar and Typo Correction")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        input_pdf_path = uploaded_file.name
        output_pdf_path = "output.pdf"

        text = extract_text_from_pdf(input_pdf_path)

        if st.button("Correct Grammar and Typos"):
            corrected_text = correct_grammar_and_typos(text)
            save_text_to_pdf(corrected_text, output_pdf_path)

            st.success("Grammar and typos corrected. Click below to download the corrected PDF file.")
            st.download_button("Download Corrected PDF", output_pdf_path,file_name='corrected_output.pdf')
            st.markdown("### Corrected Text")
            st.text_area("The corrected text is", value=corrected_text, height=200)

if __name__ == "__main__":
    main()
