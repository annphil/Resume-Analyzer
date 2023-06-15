import streamlit as st
from PyPDF2 import PdfReader
from language_tool_python import LanguageTool
from reportlab.pdfgen import canvas
import io
from io import BytesIO

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

def convert_txt_to_pdf(txt_content):
    buffer = BytesIO()

    # Create the PDF document
    p = canvas.Canvas(buffer)

    # Set the font and font size
    p.setFont("Helvetica", 12)

    # Write the content to the PDF
    p.drawString(50, 700, txt_content)

    # Save the PDF
    p.save()

    # Move the buffer's cursor back to the beginning
    buffer.seek(0)

    return buffer


def main():
    st.title("PDF Grammar and Typo Correction")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        input_pdf_path = "uploaded_pdf.pdf"

        with open(input_pdf_path, 'wb') as file:
            file.write(uploaded_file.getbuffer())

        text = extract_text_from_pdf(input_pdf_path)

        if st.button("Correct Grammar and Typos"):
            corrected_text = correct_grammar_and_typos(text)
            corrected_text_str = ' '.join(corrected_text).replace('\n', ' ')
            # save_text_to_pdf(corrected_text, output_pdf_path)

            # st.success("Grammar and typos corrected. Click below to download the corrected PDF file.")    
            st.markdown("### Corrected Text")
            st.text_area("The corrected text is", value=corrected_text_str, height=200)
            pdf_buffer = convert_txt_to_pdf(corrected_text_str)
            st.success("Conversion successful! Click below to download the PDF file.")
            st.download_button("Download PDF", pdf_buffer, file_name='converted_output.pdf')

if __name__ == "__main__":
    main()