
import streamlit as st
import os
import requests
import pandas as pd
import json
import pytesseract  # OCR
from PIL import Image
from pdf2image import convert_from_path
import tempfile

URL = "http://127.0.0.1:8000/"

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def calculate_experience_years(start_year, end_year):
    try:
        start_year = int(start_year)
        end_year = int(end_year)
        return end_year - start_year if start_year and end_year else 0
    except ValueError:
        return 0

# Streamlit UI
# لتحميل الصورة من ملف
image_path = 'srss1.png'
image = Image.open(image_path)

# لعرض الصورة في Streamlit
st.image(image, use_column_width=True)
st.title("SRS Talent Accelerators📄")
st.write("This system helps HR staff evaluate resumes to predict employee retention, assess development potential, and determine suitability for technical or administrative roles.")

uploaded_file = st.file_uploader("Upload CV's here📄", type=["pdf"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name
    
    all_text = extract_text_from_pdf(pdf_path)
    
    api_key = "sk-proj-hbHEJzUHXj1yFbc9JVwVT3BlbkFJWJk5K5fIlIHN8kGPq8Yr"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Prompt to extract main information
    prompt_main = f"""
    [no prose]
    [Output Only JSON]
    Extract the following information from the CV text:
    1. The person's name and determine the person's gender based on their name.
    2. Count the years they worked in each organization or company.
    3. Identify the start and end years of their experience in the current domain.
    4. Determine if the person stayed in each company for at least a year.
    5. Specify their education as either a [Bachelors,Masters,Diploma](must be exact same,Don't add post fixed ('s))without mentioning anything else.
    
    Here is the text:
    {all_text}

    Output the result in JSON format as follows:
    {{
      "name": "",
      "education": "",
      "experience": [
        {{
          "company": "",
          "start_year": "",
          "end_year": "",
          "years_worked": 0,
          "at_least_one_year": ""
        }}
      ],
      "gender": "",
      "current_domain_experience": {{
        "start_year": "",
        "end_year": "",
        "total_years": 0
      }}
    }}
    """

    # Prompt to extract courses and certifications
    prompt_courses = f"""
    [no prose]
    [Output Only JSON]
    Extract all the courses or certificates mentioned and determine whether the person can develop based on the number of courses or CERTIFICATIONS. If the person has more than 2 courses, they are considered capable of development.

    Here is the text:
    {all_text}

    Output the result in JSON format as follows:
    {{
      "courses": [],
      "can_develop": ""
    }}
    """

    # Prompt to extract skills
    prompt_skills = f"""
    [no prose]
    [Output Only JSON]
    Extract all the skills mentioned and determine whether the person is administrative or technical based on their skills.

    Here is the text:
    {all_text}

    Output the result in JSON format as follows:
    {{
      "skills": [],
      "role": ""
    }}
    """

    payload_main = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt_main
            }
        ],
        "max_tokens": 1500
    }

    payload_courses = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt_courses
            }
        ],
        "max_tokens": 1500
    }

    payload_skills = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt_skills
            }
        ],
        "max_tokens": 1500
    }

    # Sending requests to OpenAI API
    response_main = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload_main)
    response_courses = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload_courses)
    response_skills = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload_skills)
    
    if response_main.status_code == 200 and response_courses.status_code == 200 and response_skills.status_code == 200:
        response_json_main = response_main.json()
        response_json_courses = response_courses.json()
        response_json_skills = response_skills.json()
        
        cv_json_main = response_json_main['choices'][0]['message']['content']
        cv_json_courses = response_json_courses['choices'][0]['message']['content']
        cv_json_skills = response_json_skills['choices'][0]['message']['content']
        
        cv_data_main = json.loads(cv_json_main)
        cv_data_courses = json.loads(cv_json_courses)
        cv_data_skills = json.loads(cv_json_skills)

        # Process main data
        for exp in cv_data_main["experience"]:
            exp["years_worked"] = calculate_experience_years(exp["start_year"], exp["end_year"])
            exp["at_least_one_year"] = "Yes" if exp["years_worked"] >= 1 else "No"

        # تحقق من وجود المفتاح وتحقق من نوع البيانات
        if "current_domain_experience" in cv_data_main and "total_years" in cv_data_main["current_domain_experience"]:
            try:
                total_years = int(cv_data_main["current_domain_experience"]["total_years"])
            except ValueError:
                total_years = 0
        else:
            total_years = 0
        
        result_main = {
            #"name": cv_data_main["name"],
            "Education": cv_data_main["education"],
            "ExperienceInCurrentDomain": sum(exp["years_worked"] for exp in cv_data_main["experience"]),
            "Gender": cv_data_main["gender"],
            "EverBenched": "Yes" if total_years >= 1 else "No"
        }
        render = requests.post(URL + "predict", json=result_main)
        # st.write(render.text)

        # Process courses data
        courses = cv_data_courses.get("courses", [])
        can_develop = "Yes" if len(courses) >= 2 else "No"

        result_courses = {
            "courses": courses,
            # "Is the employee capable of development?": can_develop
            "Does the employee have potential for growth?": can_develop  
        }

        # Process skills data
        result_skills = {
            # "Skills": cv_data_skills["skills"],
            "After assessing the skills, it's clear that the employee demonstrates": cv_data_skills["role"]
        }
        
        # Display results
        st.write("Retention Rate. (Likely to Stay):")
        #st.markdown(f"**Education**: {result_main['Education']}")
        #st.markdown(f"**Experience In Current Domain**: {result_main['ExperienceInCurrentDomain']} years")
        #st.markdown(f"**Gender**: {result_main['Gender']}")
        #st.markdown(f"**Ever Benched**: {result_main['EverBenched']}")
        
        # عرض النص بخط أكبر
        st.markdown(f"<h2>{render.text}%</h2>", unsafe_allow_html=True)
        
        #st.write("Extracted Courses and Certifications:")
        #st.markdown(f"**Courses**: {', '.join(result_courses['courses'])}")
        st.markdown(f"**Does the employee have potential for growth?📉**: {result_courses['Does the employee have potential for growth?']}")
        
        #st.write("Extracted Skills:")
        st.markdown(f"""**After assessing the skills, it's clear that the employee demonstrates💼💻**: {result_skills["After assessing the skills, it's clear that the employee demonstrates"]}""")
    else:
        if response_main.status_code != 200:
            st.write(f"Failed to get main response: {response_main.status_code}")
            st.text(response_main.text)
        if response_courses.status_code != 200:
            st.write(f"Failed to get courses response: {response_courses.status_code}")
            st.text(response_courses.text)
        if response_skills.status_code != 200:
            st.write(f"Failed to get skills response: {response_skills.status_code}")
            st.text(response_skills.text)
