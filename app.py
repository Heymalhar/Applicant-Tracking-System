from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):

    if uploaded_file is not None:
        #Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        #Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts

    else:
        raise FileNotFoundError("No file uploaded.")

#Streamlit app

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume (in PDF format): ", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me About the Resume.")
# submit2 = st.button("How can I improve my skills?")
submit3 = st.button("Percentage Match.")

input_prompt1 = """

    You are an experience HR with Tech Experience in the field of any one job role from Data Science or Full Stack Web Development,
    Big Data Engineering, DEVOPS, Data Analyst. Your task is to review the provided resume against the Job Description
    for these profiles. Please share your professional evaluation on whether the candidate's profile aligns with the 
    Job role or not. Highlight the strenghts and weaknesses of the applicant in relation to the job role.


"""

# input_prompt2 = """

#     You are a Technical HR Manager with expertise in the field of Data Science, Full Stack Web Development,
#     Big Data Engineering, DEVOPS, Data Analyst. Your role is to scrutinize the resume in light of the job description provided.
#     Share your insights on the candidate's suitability for the role from an HR perspective.
#     Additionaly, offer advice on enhancing the candidate's skills and identify the areas where improvement is required.

# """

input_prompt3 = """

    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and deep ATS functionality, 
    your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
    the job description. First the output should come as percentage and then keywords missing and last final thoughts.

"""

if submit1:

    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The response is: ")
        st.write(response)

    else:
        st.write("Please upload your resume in the PDF format.")

elif submit3:

    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The response is: ")
        st.write(response)

    else:
        st.write("Please upload your resume in the PDF format.")