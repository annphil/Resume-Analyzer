import streamlit as st
import nltk # Provides functionalities like NER,POS Tagging,Tokenisation,etc.
import spacy  # spaCy is an open-source python library used for NLP functions like NER,POS tagging,etc. spacy is a python package for spaCy library
nltk.download('stopwords')
import docx2txt
from PyPDF2 import PdfReader
import PyPDF2
from pdfminer.pdfinterp import PDFResourceManager # Provides a central place to store and retrieve resources required like fonts,images,etc. for tasks like parsing.
# from PIL import Image
import pymysql # Provides a pure-Python interface for connecting and interacting with MySQL databases.
import base64 # Provides functions for encoding and decoding binary data using Base64 encoding.
from pyresparser import ResumeParser # the pyresparser library is like a magical tool that uses the ResumeParser robot to read and extract important details from resumes.
# import io
# The 'pdfminer' library provides tools for working with PDF files.
from pdfminer.converter import TextConverter # 'TextConverter' class is a specific tool within the library that specializes in converting PDFs into plain text.
# from pdfminer.layout import LAParams # A tool that helps you set parameters for layout analysis when extracting text from PDFs.
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Resume Analyzer",
    # page_icon='./Logo/SRA_Logo.ico',
)

# Load the 'en_core_web_sm' model
spacy.load('en_core_web_sm') # This line downloads a pre-trained language model for english. It processes and analyses English text 
# It saves you the effort of training your own model from scratch and provides you with a ready-to-use tool that can understand and work with English text effectively.

connection = pymysql.connect(host='localhost', user='root', password='Root1_pwd') # Establishes connection to the MySQL Software and Architecture.
cursor = connection.cursor() # Creates a cursor object to execute SQL queries. Serves as an interface for interacting with the DB.

# Function to read the text within the resume file
def resume_reader(file):
    with open(file, 'rb') as fh:
        pdf_reader = PyPDF2.PdfReader(fh)
        text = ""
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()
    return text

# Function to display resume file
def show_resume(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8') # 'b64encode()' takes binary data and encodes it using Base64 encoding. We use the decode('utf-8') method to convert it to a UTF-8 encoded string.
    resume_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>' # Used to display a PDF document within a webpage by embedding it using the <iframe> tag.
    st.markdown(resume_display, unsafe_allow_html=True)

def resume_score_calculator(resume_details,job_description_text):
    content = [job_description_text,resume_details]
    cv = CountVectorizer()
    matrix = cv.fit_transform(content)
    similarity_matrix = cosine_similarity(matrix)
    score = round(similarity_matrix[0][1]*100,2)
    return score


def run():
    st.title("Resume Analyzer")
    st.sidebar.markdown("# Choose User") # To display a heading in the sidebar with the text "Choose User".
    activities = ["Applicant", "Admin"]
    choice = st.sidebar.selectbox("Choose from the options:", activities) # To create a dropdown select box widget.
    #img = Image.open('./Logo/SRA_Logo.jpg')
    #img = img.resize((250, 250))
    #st.image(img) # MAKE CHANGES TO IMAGE PATH AND SIZE AS PER REQUIREMENT

    # Create the DB
    db_sql = """CREATE DATABASE IF NOT EXISTS RESUME_ANALYSIS"""
    cursor.execute(db_sql)
    connection.select_db("RESUME_ANALYSIS")

    # Create table
    DB_table_name = 'User_Data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(100) NOT NULL,
                     Email_ID varchar(50) NOT NULL,
                     Resume_Score varchar(8) NOT NULL,
                     Predicted_Field varchar(25) NOT NULL,
                     Current_Skills varchar(300) NOT NULL,
                     Recommended_Skills varchar(300) NOT NULL,
                     Recommended_Courses varchar(300) NOT NULL,
                     PRIMARY KEY(ID));
                    """ 
    cursor.execute(table_sql)
    if choice == "Applicant":
        resume_file = st.file_uploader("Choose your Resume", type=["pdf"])
        job_description = st.text_input("Enter the Job Description: ")
        if resume_file is not None:
            save_file_path = './Uploaded_Resumes/' + resume_file.name
            with open(save_file_path,"wb") as f: # Here, we create a special box for writing and saving our work. 'wb' means we can write and save information of any kind (b-binary).
                f.write(resume_file.getbuffer()) # We retrieve data in a specific format using 'getbuffer()' and write it to our file.
            show_resume(save_file_path)
            resume_data = ResumeParser(save_file_path).get_extracted_data() # It extracts information from the resume and stores it in the 'resume_data' variable.
            if resume_data:
                # Getting the whole resume data
                resume_text = resume_reader(save_file_path)

                st.header("**Resume Analysis**")
                st.success("Hello " + resume_data['name'])
                st.subheader("**Your Basic info**")
                try:
                    st.text('Name: ' + resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Name: ' + resume_data['mobile_number'])
                except:
                    pass   
                resume_score = resume_score_calculator(resume_text,job_description) 
                st.info(f"Your resume score is: {resume_score}%")
                candidate_level=''

run()
